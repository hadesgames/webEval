from webEval.web_eval__core.models import *
from webEval.web_eval__core.utils__helper import *

def upload_input_file (file, problem, test):
    input_filename = '%s-%s.in' % (test.no, problem.code)
    input_path = os.path.join(settings.TESTS_DIR, problem.code, input_filename)
    save_file(input_path, file)
    test.input_size = file.size
    test.save()
    os.system("svn add %s" % input_path)
    
    
def upload_output_file (file, problem, test):
    output_filename = "%s-%s.ok" % (test.no, problem.code)
    output_path = os.path.join(settings.TESTS_DIR, problem.code, output_filename)
    save_file(output_path, file)
    test.output_size = file.size
    test.save()
    os.system("svn add %s" % output_path)
