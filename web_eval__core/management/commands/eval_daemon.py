import os, shutil

from django.core.management.base import BaseCommand, CommandError
from webEval.settings import *
from webEval.web_eval__core.models import *

class Command(BaseCommand):
    help = 'Extracts jobs from db.'

    def handle(self, *args, **options):
        while True:
            try:
                job = Job.objects.filter(processing = False, percent_completed = 0)[0]
            except:
                time.sleep(2)
                continue
            
            print "Job %d: problem %s, contest %s" % (job.id, job.problem.code, job.contest.code),
            job.processing = True
            job.save()
        
            # call grader
            shutil.copy(os.path.join(JOBS_DIR, 'job%d.%s' % (job.id, job.language)),
                        os.path.join(EVAL_DIR, 'stud', job.user.username, '%s.%s' % (job.problem.code, job.language)))
            os.system("%s -- %s %s" % (os.path.join(EVAL_DIR, 'grader.py'), job.problem.code, job.user.username))
            os.remove(os.path.join(EVAL_DIR, 'stud', job.user.username, "%s.%s" % (job.problem.code, job.language)))
                            
            job.processing = False
            job.percent_completed = 100
            job.save()
            print "Completed: %s" % job.message
            
                
                