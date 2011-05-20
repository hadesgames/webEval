import datetime
import hashlib
import random

from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse

from webEval.web_eval__core.models import *
from webEval.settings import HOST_URL

class Command(BaseCommand):
    help = 'Creates default entries in database, like default contest, default blog entry, etc'

    def handle(self, *args, **options):
        # Make the first user in system admin.
        
        for job in Job.objects.all():
            job.score = sum([y.score for y in Test.objects.filter(job=job)])
            job.message = "Completed: %d points" % job.score
            job.save()
            """ 
            for test in xrange(1, 21):
                t = Test()
                t.job = job
                t.no = test
                t.score = random.choice([0, 5])
                t.message = "Okay!!!" if t.score else "Wrong answer in: adunare.out"
                t.time = random.choice([0, 4, 8])
                t.memory = random.choice([8, 12])
                t.save()
            """