from annoying.functions import get_object_or_None
from django.contrib.sessions.models import Session, SessionStore
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from webEval.api.models import *
from webEval.web_eval__core.models import *
from webEval.web_eval__core.auth__helper import user_auth

import xml.dom.minidom

def create_eval (request):
    user = user_auth(request)
    
    if user.has_perm('api.add_eval') is False:
        return redirect_to_index('You don\'t have permission to add evals.')
    
    if request.method == 'POST':
        form = CreateEvalForm(request)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('')
    else:
        form = CreateEvalForm()
        
    return render_to_response('api/create_eval.html',
                              {'form' : form },
                              context_instance = RequestContext(request)
                             )
    
            
@csrf_exempt
def login (request):
    if request.method == 'POST':
        public_key = request.POST['public_key'] if 'public_key' in request.POST else None
        message = request.POST['login_message'] if 'login_message' in request.POST else None
                
        eval = get_object_or_None(Eval, public_key = public_key)
        
        if eval is not None and message is not None:
            if eval.server_decode(message) == 'Login':
                s = SessionStore()
                s['eval_id'] = eval.id
                s.save()
                
                message = s.session_key, 0
            else:
                message = 'Password didn\'t match', 1
        else:
            message = 'Wrong query', 2
    else:
        message = 'Wrong query', 2
    
    return render_to_response('api/login.xml',
                              {'message' : message},
                              context_instance = RequestContext(request)
                             )
    

@csrf_exempt
def return_job (request):
    print "okay"
    if request.method == 'POST':
        session_key = request.POST['session_key'] if 'session_key' in request.POST else None
        session = get_object_or_None(Session, session_key = session_key)
        eval = get_object_or_None(Eval, id=session.get_decoded()['eval_id'])
        
        if eval is not None:
            try:
                job = Job.objects.filter(processing = False, percent_completed = 0).order_by('id')[0]
                job.processing = True
                job.percent_completed = 0
                job.message = "Processing..."
                job.save()
                
                message = "Okay", 0
            except:
                job = None
                message = "Job doesn't exist, try again, later", 1
        else:
            message = 'Wrong query', 2
            job = None
    else:
        message = 'Wrong query', 2
        job = None
                
    return render_to_response('api/return_job.xml',
                              {'job' : job,
                               'message' : message,
                               'updated' : eval.updated if eval is not None else False,
                              },
                              context_instance = RequestContext(request)
                             )
            
            
@csrf_exempt
def update_job (request):
    if request.method == 'POST':
        session_key = request.POST['session_key'] if 'session_key' in request.POST else None
        session = get_object_or_None(Session, session_key = session_key)
        eval = get_object_or_None(Eval, id=session.get_decoded()['eval_id'])
        request_xml = request.POST['request'] if 'request' in request.POST else None
        
        #print request_xml
        
        if eval is not None and request_xml is not None:
            doc = xml.dom.minidom.parseString(request_xml)
            request_tag = doc.getElementsByTagName('request')[0]
            job_tag = request_tag.getElementsByTagName('job')[0]
            #print request_tag
            #print job_tag
            message = job_tag.getElementsByTagName('message')[0].childNodes[0].toxml()
            job_id = job_tag.getElementsByTagName('id')[0].childNodes[0].toxml()
            #print message
            #print job_id
            score = job_tag.getElementsByTagName('score')[0].childNodes[0].toxml()
            #print score
            compile_message = job_tag.getElementsByTagName('compile')[0].childNodes[0].toxml()
            
            #print compile_message
            
            job = get_object_or_None(Job, id = job_id)
            
            #print "job_id :%s " % job_id
            #print "message : %s"  % message
            
            if job is not None:
                job.message = message
                job.score = score
                job.save()
            
                #print "OKAY"
                Test.objects.filter(job = job).delete()
                #print "OKAY"
                
                for test in job_tag.getElementsByTagName('test'):
                    t = Test(job = job)
                    #print job.id
                    t.no = test.getElementsByTagName('id')[0].childNodes[0].toxml()
                    #print t.no
                    t.time = test.getElementsByTagName('time')[0].childNodes[0].toxml().rstrip('ms')
                    #print t.time
                    t.memory = test.getElementsByTagName('memory')[0].childNodes[0].toxml().rstrip('kb')
                    #print t.memory
                    t.score = test.getElementsByTagName('score')[0].childNodes[0].toxml()
                    #print t.score
                    t.message = test.getElementsByTagName('message')[0].childNodes[0].toxml()
                    #print t.message
                    t.save()
                    #print "SAVED"
                    
                job.processing = False
                job.percent_completed = 100
                job.save()
                
                #print "OKAY 1"
                sc = get_object_or_None(ScoreCache, contest = job.contest, user = job.user)
                if sc is None:
                    sc = ScoreCache(contest = job.contest, user = job.user)
                    sc.save()
                    
                #print job.contest
                #print sc.contest.code
                
                #print "OKAY 2"    
                spc = get_object_or_None(ScoreProblemCache, cache = sc, problem = job.problem)
                if spc is None:
                    spc = ScoreProblemCache(cache = sc, problem = job.problem, score = job.score)
                    spc.save()
                else:
                    spc.score = job.score
                    spc.save()
                #print "okay 3"
                sc.build()
                
            else:
                message = 'Job doesn\'t exist', 1
    
            message = 'Okay', 0
        else:
            message = 'Wrong query', 2
    else:
        message = 'Wrong query', 2
            
    return render_to_response('api/update_job.xml',
                              {' message' : message},
                              context_instance = RequestContext(request))
        
def get_your_score (request):
    user = user_auth(request)
    problem_id = request.GET['problem_id'] if 'problem_id' in request.GET and request.GET['problem_id'] != '' else None
    contest_id = request.GET['contest_id'] if 'contest_id' in request.GET and request.GET['contest_id'] != '' else None
    score_only = True if 'score_only' in request.GET else False
    
    if problem_id is None or contest_id is None or user is None:
        result = 'N/A'
    else:
        problem = get_object_or_None(Problem, id = problem_id)
        contest = get_object_or_None(Contest, id = contest_id)
        
        if problem is None or contest is None:
            result = 'N/A'
        elif contest.ended is False and contest.with_open_eval is False:
            result = 'N/A'
        else:
            jobs = Job.objects.filter(user = user, problem = problem, contest = contest).order_by('-id')
            if jobs:
                result = str(jobs[0].score) if score_only else "%d points" % jobs[0].score
            else:
                result = 'N/A'
    if result == 'N/A':
        result = '<span style="font-size: 0.8em; color: #808080;">N/A</span>'
    return HttpResponse(result)


def check_if_username_exists (request):
    if request.is_ajax():
        if request.method == 'GET':
            username = request.GET['username'] if 'username' in request.GET else None
            if UserProfile.objects.filter(username = username):
                return HttpResponse("True")
    return HttpResponse("False")