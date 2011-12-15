from piston.handler import BaseHandler
from webEval.web_eval__core.models import Job

class JobHandler(BaseHandler):
    allowed_methods = ('GET', 'PUT', )
    model = Job

    def read(self, request):
        print "read ", attrs
        return Job.objects.filter(processing=False, percent_completed=0)

    def update(self, request):
        """ Edit a job.  """
        attrs = self.flatten_dict(request.POST)
        print "UPDATE ", attrs, request.user
        
        print attrs['id']
        user = request.user
        
        return Job.objects.get(id=attrs['id'])    
    
    