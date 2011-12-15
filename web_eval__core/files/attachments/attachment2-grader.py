#!/usr/bin/env python


#################################################################################
#                          Grader rewrite, version 0.99                         #
#===============================================================================#
#                   Made by Teodor Anton Pripoae and Dan Sanduleac              #
#                            Distributed under GNU GPL                          #
#################################################################################

import sys
import os
import shutil
from os.path import join, abspath, dirname, isfile, isdir

BaseDir = abspath(dirname(sys.argv[0]))

sys.path.insert(0, join(BaseDir, 'scripts'))
sys.path.insert(0, join(BaseDir, 'scripts', 'eval2'))
# config must have paths relative to this dir now
# note that it was different for taskeval-launcher which was in scripts/
# -- very important, import the configuration first
import config
import taskeval
from taskeval.evalcore import EvalError, die as eval_die
import subprocess
import shutil
from StringIO import StringIO

global_grading = False
where_interrupted = False
job_number = 0

# This will be like a map of already loaded problems
problems = {}

# ------------------------------------------------------------

# This may or may not remain in the working code
# Method three of loading configuration file

#class Round:
#
#    __params__ = ['problems', 'students']
#        
#    def __validate_param(self, x):
#        return x[0] in self.__params__
#
#    def __init__(self, name):
#        config_file = 'contest/%s/%s_config.py' % (name, name)
#        exec compile(open(config_file).read(), '/dev/null', 'exec')
#
#        self.__dict__.update(
#            filter(self.__validate_param, locals().items())
#        )

# HELPER CLASSES
# ===========================================

# make EvalError a type of GraderError

# GraderError is always handled, but I wanted this behaviour
# because in the event of an EvalError occuring, it should kill
# the whole grader unless explicitly caught in time

class GraderError(Exception):
    'Critical error, causes whole grader to die'
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return (isinstance(self.value, str) \
            and self.value or str(self.value))

class EvalError(GraderError):
    pass

taskeval.evalcore.EvalError = EvalError

# HELPER FUNCTIONS
# ===========================================

def ternary (condition, if_do, else_do):
    if condition:
        return if_do
    return else_do


def short_write(message):
    sys.stdout.write(message)
    sys.stdout.flush()


def grader_die(message):
    raise GraderError(message)


def import_from(path, name):
    sys.path.insert(0, path)
    exec("import %s as r" % name)
    del sys.path[0]
    return r


def import_object(path, name, params):
    '''Imports ./path/name.py and checks that it contains the given params'''
    try:
        # Loading code
        r = import_from(join(BaseDir, path), name)

        # Sanity check
        for param in params:
            getattr(r, param)
    except (AttributeError, ImportError), e:
        grader_die("%s in loading \"%s/%s\": %s" % (type(e).__name__, path, name, str(e)))

    # Embed the round/problem/whatever's name
    r.name = name

    return r


# HEAVY LOAD FUNCTIONS
# ===========================================

def load_problem(prob):
    'Loads a problem by instantiating the Problem class and then caches it'
    # So far, cache just by the name of the problem
    # Can confuse problems if path depths are allowed!
    # FIXME later

    # TODO: check type of problem, implement interactive problem
    # in taskeval
    if prob not in problems:
        try:
            problems[prob] = taskeval.evalcore.Problem(path = prob + '/', \
                verif = join(dirname(sys.argv[0]), 'prob', prob, 'judge'))
        # If we cannot instantiate a problem, it becomes a grader-wide issue
        except EvalError, err:
            grader_die(str(err))
    return problems[prob]


def compile_student_source(stud, prob):
    '''Compiles the source code for student "stud/$stud" for the problem $prob'''

    short_write("[compiling: ")

    path = join(BaseDir, 'stud', stud, prob)    # path to source without extension
    makefile_path = join(BaseDir, 'prob', prob, 'makefile') # path to problem's makefile
    makefile_sample_path = join(BaseDir, 'scripts', 'sample_makefile') # path to sample makefile
    makefile_work_path = join(BaseDir, 'work', 'makefile')  # path to where makefile should be put
#    compile_command = {
#        '.c'   : "gcc -Wall -O2 -static %s.c -o work/the.exe -lm" % path,    # gcc command
#        '.cpp' : "g++ -Wall -O2 -static %s.cpp -o work/the.exe -lm" % path,  # g++ command
#        '.pas' : "fpc -O2 -Xs %s.pas -owork/the.exe" % path,                 # fpc command
#    }
    extension = 'no source file'                                                         # student has no source file

    for iterator in ['.adb', '.bas', '.bf', '.c', '.cs', '.cpp', '.d', '.java', '.lua', '.ocaml', '.pas', '.pike', '.pl', '.php', '.py', '.py3', '.rb', '.tcl']:
        if os.path.isfile(path + iterator):
            extension = iterator

    if extension == 'no source file':    # student does not have source file
        # aborting evaluation for this user on this problem
        print 'error]'
        eval_die("Student %s doesn't have any source for problem %s" % (stud, prob) )

    our = os.path.isfile(makefile_path + extension)
    sample = os.path.isfile(makefile_sample_path + extension)
    if our or sample:
        shutil.copy(ternary(our, makefile_path + extension, makefile_sample_path + extension), makefile_work_path)
        shutil.copy(path + extension, join(BaseDir, 'work/user' + extension))
        os.chdir('work')
        process = subprocess.Popen('make -s', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        compiler_message = process.communicate() [0]
        returncode = process.returncode
        os.chdir('..')
    else:
        print 'error]'
        eval_die("I don't have compile support for %s extension. I can't judge student %s on problem %s" % (extension, stud, prob))

    returncode = process.returncode
    if returncode != 0:
        print 'error]'
    else: short_write("ok] ")
    return (returncode, compiler_message)


def load_round(round_name):
    print "============ Loading Round", round_name, "============"
    __params__ = ['problems', 'students']
    # sanity check - round_name should be valid name
    if not round_name.isalnum() or not round_name[0].isalpha():
        grader_die("Couldn't load round %s, invalid name.\nPlease use only letters and numbers, first character letter" % round_name)
    return import_object('contest', round_name, __params__)


def grade_round(round):
    # TODO: introduce some finally here to do the cleanup
    # in case we get KeyboardInterrupted
    global global_grading
    global where_interrupted
    global job_number
    global_grading = True
    where_interrupted = False
    job_number = 0

    interrupted_file_path = os.path.join(BaseDir, 'interrupted.log')

    if isfile(interrupted_file_path):
        interrupted_file = open(interrupted_file_path, 'r')
        where_interrupted = interrupted_file.readline()
        where_interrupted = int(where_interrupted)
        interrupted_file.close()
        os.remove(interrupted_file_path)

    if isfile('allres.txt'): os.remove('allres.txt')
    if isfile('scores-tmp.txt'): os.remove('scores-tmp.txt')
    if isfile('scores.txt'): os.remove('scores.txt')
    # TODO: this really has to get pythonized
    os.system('bash scripts/print_script.sh STUDENT')

    for nr, problem in enumerate(round.problems):
        # TODO: same as above
        os.system('bash scripts/print_script.sh "%s" %d' % (problem, nr+1))

    for nr, problem in enumerate(round.problems):
        print '******* Problem: %s [%d of %d]' % (problem, nr+1, len(round.problems))
        for nr, student in enumerate(round.students):
            print '[processing %d of %d] %s: ' % (nr+1, len(round.students), student),
            sys.stdout.flush()
            grade_student(student, problem)
            print

    os.system('echo "TOTAL" >> scores-tmp.txt')
    for student in round.students:
        s = ' '.join(round.problems)
        os.system('bash scripts/merge_all_res.sh "%s" %s' % (student, s))

    # sort scores.txt into scores-tmp.txt
    # ce dubios !!! TODO, make it python
    os.system('sort -k %dnr scores.txt >> scores-tmp.txt' % (len(round.problems)+2))
    os.rename('scores-tmp.txt', 'scores.txt')
    shutil.copy('allres.txt', join('contest', round.name))
    shutil.copy('scores.txt', join('contest', round.name))
    

def copy_results(stud, prob):
    run_tmp = join(BaseDir, 'work/run.tmp')
    if isfile(run_tmp):
        shutil.copy(run_tmp, join(BaseDir, 'stud/%s/%s.tmp' % (stud, prob)))
    elif isfile(join(BaseDir, 'stud/%s/%s.tmp') % (stud, prob)):
        open(join(BaseDir, 'stud/%s/%s.tmp') % (stud, prob), 'w').close() 

    compile_tmp = join(BaseDir, 'work/compile')
    if isfile(compile_tmp):
        shutil.copy(compile_tmp, join(BaseDir, 'stud/%s/%s-compile.tmp') % (stud, prob))
    elif isfile(join(BaseDir, 'stud/%s/%s-compile.tmp')):
        open(join(BaseDir, 'stud/%s/%s-compile.tmp') % (stud, prob), 'w').close()


def grade_student(stud, prob):
    # TODO return score
    '''Grade the student in "stud/$stud" on the problem $prob
    @returns score ?
    '''
    global job_number

    def sanity_check(student_dir, prob):
        if not isdir(student_dir):
            eval_die("Student %s doesn't exist in stud/" % stud)
        elif not filter(lambda x: x.startswith(prob), os.listdir(student_dir)):
            eval_die("Couldn't find any source code for student '%s' that would match problem %s" % (stud, prob))

    if global_grading is False:
        print "Grading student %s on problem %s" % (stud, prob)
    else:
        job_number += 1
        if where_interrupted and job_number < where_interrupted:
            return

    # FIXME
    # __params__ = i dunno
    # r = import_object('prob', prob, __params__)

    student_dir = join(BaseDir, 'stud', stud)

    try:
        sanity_check(student_dir, prob)

        problem = load_problem(prob)

        # Save the output somewhere
        output = taskeval.consoleapp.main_output = StringIO()
        if not global_grading:
            output.isatty = lambda: True

        if problem.opts['type'] == 'classical':
            returncode, compiler_message = compile_student_source(stud, prob)
            # TODO: save compiler_message somewhere
            compile_output_file = open(os.path.join(BaseDir, 'work', 'compile'), 'w')
            compile_output_file.writelines(compiler_message)
            compile_output_file.close()
            if returncode != 0:
                eval_die("Compile error")

            # evaluate the executable
            # the join BaseDir is "just in case", cause we chdir to BaseDir anyway
            score = taskeval.consoleapp.print_results(problem, join(BaseDir, "work", "the.exe"))
        elif problem.opts['type'] == 'output-only':
            score = taskeval.consoleapp.print_results(problem,
                join(student_dir, "%s-out" % prob), user_output = "?-%s.out")
        elif problem.opts['type'] == 'interactive':
            pass

        # TODO: save `output` somewhere
        eval_output_file = open(os.path.join(BaseDir, 'work', 'run.tmp'), "w")
        print >> eval_output_file, output.getvalue()
        eval_output_file.close()

        if global_grading is False:
            print '\nShowing compile details:\n'
            print compiler_message
            print 'Showing allres:\n'
            print output.getvalue()
            
    except EvalError, e:
        # handle the error
        print >>sys.stderr, 'Evaluation error:', e
    finally:
        copy_results(stud, prob)


def clear_all(mkdir = True):
    'Deletes and recreates the ./work dir'
    if os.path.isdir(join(BaseDir, 'work')):
        shutil.rmtree(join(BaseDir, 'work'))

    if mkdir:
        os.mkdir(join(BaseDir, 'work'))


def log_when_stopped():
    file = open(os.path.join(BaseDir, 'interrupted.log'), 'w')
    file.writelines(str(job_number))
    file.close()


def main(argv):

    clear_all()
    
    os.chdir(BaseDir)

    assert len(argv) > 0 and argv[0]

    myname = os.path.basename(argv[0])
    USAGE = """EVALUATOR: usage:
    \t./%s <day-to-evaluate>    -or-
    \t./%s -- <problem> <contestant>\n""" % (myname, myname)


    # logs just errors, to stdout
    taskeval.consoleapp.configure_output(verbosity = 1)
    #taskeval.consoleapp.configure_output(verbosity = 1, log_output = '.')


    def die_usage():
        print USAGE
        sys.exit(1)

    # ---------------------------------------
    # actual parsing
    # ---------------------------------------
    if len(argv) < 2:
        die_usage()

    # Round
    if len(argv) < 3:
        if argv[1] == '--':
            die_usage()
        grade_round( load_round(argv[1]) )

    else:
        if not argv[3:4]:
            die_usage()
        grade_student(argv[3], argv[2])
        
        """
        # show compile details
        print "Showing compile details:"
        os.sys("cat stud/%s/%s-compile.tmp" % (argv[2], argv[3]))
        
        # show allres
        print "Showing allres:"
        os.sys("cat stud/%s/%s.tmp" % (argv[2], argv[3]))
        """

    clear_all(mkdir = False)


if __name__ == '__main__':
    try:
        sys.exit(main(sys.argv))
    except GraderError, e:
        print >>sys.stderr, 'Critical error:', e
    except KeyboardInterrupt:
        print >>sys.stderr, '\nInterrupted, cleaning up'
        log_when_stopped()

    sys.exit(1)
