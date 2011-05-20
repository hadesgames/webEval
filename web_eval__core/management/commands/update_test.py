import os, shutil
from annoying.functions import get_object_or_None
from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from webEval.settings import *
from webEval.web_eval__core.models import *

class Command(BaseCommand):
    help = 'Updates tests in db.'

    option_list = BaseCommand.option_list + (
        make_option('--job_id', dest='job_id', action='store', default=False, help="Job id"),
        make_option('--test_id', dest='test_id', action='store', default=False, help="Test id"),
        make_option('--score', dest='score', action='store', default=False, help="Test score"),
        make_option('--time', dest='time', action='store', default=False, help="Execution time"),
        make_option('--memory', dest='memory', action='store', default=False, help="Memory usage"),
        make_option('--message', dest='message', action='store', default=False, help="Test message")
    )
    
    def handle(self, *args, **options):
        test_id = options.get('test_id') if options.get('test_id') else None
        job_id = options.get('job_id') if options.get('job_id') else None
        score = options.get('score') if options.get('score') else None
        time = options.get('time') if options.get('time') else None
        memory = options.get('memory') if options.get('memory') else None
        message = options.get('message') if options.get('message') else None
        print "Updating test %s on job %s with score %s, time: %sms, memory %skb, message: %s" % (test_id, job_id, score, time, memory, message)
        
        if test_id is None or job_id is None or score is None or time is None or memory is None or message is None:
            return
        
        job = get_object_or_None(Job, id = job_id)
        Test.objects.filter(job = job_id, no = test_id).delete()
        Test(job=job, no = test_id, score = score, message = message, time = time, memory = memory).save()