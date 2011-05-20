import datetime
import os

from annoying.functions import get_object_or_None

from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.core.urlresolvers import resolve
from django.template import RequestContext, Context
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.csrf import csrf_protect

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from webEval import judge_settings
from webEval.settings import JOBS_DIR, TESTS_DIR
from webEval.api.models import Eval
from webEval.web_eval__core.auth__helper import user_auth
from webEval.web_eval__core.grader__helper import *
from webEval.web_eval__core.models import *
from webEval.web_eval__core.utils__controller import redirect_to_index
from webEval.web_eval__core.utils__helper import *
from webEval.web_eval__core.wiki__controller import edit_page, display_revision
from webEval.web_eval__core.wiki__helper import create_problem_wiki_page, create_contest_wiki_page

@login_required
def create_problem (request):
    user = user_auth(request)
    
    if not user.has_perm('web_eval__core.add_problem'):
        return redirect_to_index("You don't have permission to add problems.")
        
    if request.method == 'POST':
        form = ProblemCreateForm(request.POST)
        if form.is_valid():
            contest = Contest.objects.get(code = 'none')
            
            problem = form.save(commit = False)
            
            problem.name = problem.code
            problem.owner = user
            problem.resource = contest
            
            try:
                problem.author = Author.objects.get(name = '%s %s' % (user.first_name, user.last_name))
            except:
                author = Author(name = '%s %s' % (user.first_name, user.last_name),
                       code = '%s_%s' % (user.first_name, user.last_name))
                author.save()
                problem.author = author
            
            problem.time_limit = judge_settings.DEFAULT_TIME_LIMIT
            problem.memory_limit = judge_settings.DEFAULT_MEMORY_LIMIT
            problem.source_limit = judge_settings.DEFAULT_SOURCE_LIMIT
            
            problem.forum_topic = None
            problem.wiki_page = create_problem_wiki_page(problem, request)
            problem.type = 'Normal'
            
            problem.save()
            
            contest.problems.add(problem)
            contest.save()
            
            os.system("mkdir %s" % os.path.join(TESTS_DIR, problem.code))
            os.system("touch %s" % os.path.join(TESTS_DIR, problem.code, 'tests.txt'))
            os.system("svn add %s" % os.path.join(TESTS_DIR, problem.code))
            
            return HttpResponseRedirect(reverse('webEval.web_eval__core.grader__controller.configure_problem',
                                                kwargs={'problem_code' : problem.code}
                                               )
                                       )
    else:
        form = ProblemCreateForm()
        
    return render_to_response("grader/create_problem.html",
                             {
                                'form' : form,
                                'navigation' : 
                                {
                                    'main' : 'admin', 
                                    'other' : 'create-problem'
                                }
                             },
                             context_instance=RequestContext(request))
    

@login_required
def create_contest (request):
    user = user_auth(request)
    
    if not user.has_perm('web_eval__core.add_contest'):
        return redirect_to_index("You don't have permission to add contests.")
    
    if request.method == 'POST':
        form = ContestCreateForm(request.POST)
        if form.is_valid():
            contest = form.save(commit = False)
            
            contest.name = contest.code
            contest.start_time = datetime.datetime.now()
            contest.end_time = contest.start_time + datetime.timedelta(days=1)
            contest.with_rating = False
            contest.with_open_eval = False
            contest.wiki_page = create_contest_wiki_page(contest, request)
            contest.save()
            
            return HttpResponseRedirect(reverse('webEval.web_eval__core.grader__controller.display_contest',
                                                kwargs = {'contest_code' : contest.code }))
            
    else:
        form = ContestCreateForm()
        
    return render_to_response("grader/create_contest.html",
                              {
                                    'form': form,
                                    'navigation' : 
                                    {
                                        'main' : 'admin', 
                                        'other' : 'create-contest'
                                    }
                              },
                              context_instance = RequestContext(request)
                             )


@login_required
def configure_contest (request, contest_code):
    user = user_auth(request)
    
    if user.has_perm('web_eval__core.edit_contest') is False:
        return redirect_to_index("You don't have permission to edit contests.")
    
    contest = get_object_or_404(Contest, code = contest_code)
    
    message = ""
    
    if request.method == 'POST':
        form = ContestEditForm(request.POST, instance = contest)
        if form.is_valid():
            form.save()
            contest.problems.remove()
            print request.POST
            for problem_id in request.POST.getlist('selected_problems'):
                problem = get_object_or_None(Problem, id = problem_id)
                print problem_id
                if problem is not None:
                    contest.problems.add(problem)
            contest.save()
            message = "Contest successfully saved."
            form = ContestEditForm(contest)
    else:
        form = ContestEditForm(contest)
    
    #print form.data['start_time']
    return render_to_response('grader/configure_contest.html',
                              {
                                    'contest' : contest,
                                    'all_problems' : Problem.objects.all(),
                                    'form' : form,
                                    'message' : message,
                                    'navigation' : {
                                        'main' : 'admin',
                                        'other': 'edit-contest',
                                    }
                              },
                              context_instance = RequestContext(request))
    
    
@login_required
def configure_problem (request, problem_code):
    user = user_auth(request)
    
    if user.has_perm('web_eval__core.edit_problem') is False:
        return redirect_to_index("You don't have permission to edit problems.")
    
    problem = get_object_or_404(Problem, code = problem_code)
    tests = GraderTest.objects.filter(problem = problem).order_by('no')
    
    message = ""
    
    if request.method == 'POST':
        if 'testid' in request.POST:
            if request.POST['testid'] == '':
                form = ProblemEditForm(problem)
            else:
                form = ProblemEditForm(problem)
                test_id = request.POST['testid']
                
                test = get_object_or_None(GraderTest, problem = problem, no = test_id)
        
                if test is None:
                    test = GraderTest(problem = problem, no = test_id)
                    test.save()
            
                if 'inputfile' in request.FILES and request.FILES['inputfile'] != '':
                    upload_input_file(request.FILES['inputfile'], problem, test)
                
                if 'outputfile' in request.FILES and request.FILES['outputfile'] != '':
                    upload_output_file(request.FILES['outputfile'], problem, test)
                    
                message = "Tests succesfully uploaded."
                
                for eval in Eval.objects.all():
                    eval.updated = True
                    eval.save()
                    
                tests_file = open(os.path.join(TESTS_DIR, problem.code, 'tests.txt'), 'w')
                tests = GraderTest.objects.filter(problem = problem)
                for test in tests:
                    print >> tests_file, "%s %d" % (test.no, 100 / len(tests))
                tests_file.close() 
                    
                os.system("svn commit %s -m \"Test %s for problem %s\"" % (TESTS_DIR, test_id, problem.code))
        else:
            resource = problem.resource
            form = ProblemEditForm(request.POST, instance = problem)
            
            if form.is_valid():
                form.save()
                
                if problem.resource != resource:
                    problem.resource.problems.add(problem)
                    problem.resource.save()
                
                message = "Problem successfully saved."
                form = ProblemEditForm(problem)
    else:
        form = ProblemEditForm(problem)
        
    return render_to_response('grader/configure_problem.html',
                              {
                                    'problem' : problem,
                                    'contests' : Contest.objects.all(),
                                    'tests' : tests,
                                    'form' : form,
                                    'message' : message,
                                    'navigation' : {
                                        'main' : 'admin',
                                        'other' : 'configure-problem',
                                    }
                              },
                              context_instance = RequestContext(request))
    

@login_required
def edit_problem_statement (request, problem_code):
    problem = get_object_or_404(Problem, code = problem_code)
    return edit_page (request, 
                      page_url = problem.wiki_page.url, 
                      widgets = {
                            'is_problem' : True,
                            'problem' : problem,
                      }
                     )
    
@login_required
def edit_contest_statement (request, contest_code):
    contest = get_object_or_404(Contest, code = contest_code)
    return edit_page (request, 
                      page_url = contest.wiki_page.url, 
                      widgets = {
                            'is_contest' : True,
                            'contest' : contest,
                      }
                     )
    

@login_required
def edit_problem_tags (request, problem_code):
    user = user_auth(request)
    
    if user is None or user.has_perm('web_eval__core.edit_problem') is False:
        return redirect_to_index("You don't have permission to edit problems.")
    
    problem = get_object_or_404(Problem, code = problem_code)
    return render_to_response('grader/edit_problem_tags.html',
                              {
                                    'problem' : problem,
                                    'navigation' : {
                                        'main' : 'judge',
                                        'other' : 'edit-problem-tags',
                                    }
                              },
                              context_instance = RequestContext(request)
                             )


def display_problem (request, problem_code):
    user = user_auth (request)
    problem = get_object_or_404 (Problem, code = problem_code)
    
    return display_revision(revision = problem.wiki_page.last_revision,
                            user = user,
                            widgets = {
                                            'is_problem' : True,
                                            'problem' : problem,
                                            'submit_form' : JobSubmitForm(),
                                            'compilers' : judge_settings.COMPILERS,
                                      },
                            context_instance = RequestContext(request),
                           )
    
def display_contest (request, contest_code):
    user = user_auth (request)
    contest = get_object_or_404 (Contest, code = contest_code)
    
    return display_revision(revision = contest.wiki_page.last_revision,
                            user = user,
                            widgets = {
                                            'is_contest' : True,
                                            'contest' : contest,
                                      },
                            context_instance = RequestContext(request),
                           )


@login_required
def display_job (request, job_id):
    user = user_auth (request)
    job = get_object_or_404(Job, id=job_id)
    
    if job.can_view(user) is False:
        return redirect_to_index("You don't have permission to view this job")
        
    return render_to_response("grader/display_job.html",
                              {
                                    'job' : job,
                                    'tests' : Test.objects.filter(job=job).order_by('no'),
                                    'navigation' : {
                                        'main' : 'judge',
                                        'other' : 'display-job',
                                    }
                              },
                              context_instance = RequestContext(request))
    

@login_required
def display_job_source_code (request, job_id):
    user = user_auth (request)
    job = get_object_or_404(Job, id=job_id)
    
    if job.can_view_source_code(user) is False:
        return redirect_to_index("You don't have permission to view this job's source code")
        
    lexer = get_lexer_by_name(pygments_standardize(job.language), stripall=True, tabsize=4)
    formatter = HtmlFormatter(linenos=True)
    source_code = highlight(''.join(open(os.path.join(JOBS_DIR, 'job%d.%s' % (job.id, job.language)), 'r').readlines()), lexer, formatter)

    return render_to_response("grader/display_job_source_code.html",
                              {
                                'job' : job,
                                'source_code' : source_code,
                                'navigation' : {
                                    'main' : 'judge',
                                    'other' : 'display-job-source',
                                }
                              },
                              context_instance = RequestContext(request))


def status (request):
    user, problem, contest = None, None, None
    current_user = user_auth(request)
    
    if request.method == 'GET':
        user = get_object_or_None(User, username = request.GET['user']) if 'user' in request.GET else None
        problem = get_object_or_None(Problem, code = request.GET['problem']) if 'problem' in request.GET else None
        contest = get_object_or_None(Contest, code = request.GET['contest']) if 'contest' in request.GET else None
        score_begin = int(request.GET['score_begin']) if 'score_begin' in request.GET else 0
        score_end = int(request.GET['score_end']) if 'score_end' in request.GET else 100
        page_ind = int(request.GET['page']) if 'page' in request.GET else 1
        reeval = True if 'reeval' in request.GET else False
        
    kwargs = { } 
    url = []
    
    if user is not None:
        kwargs['user'] = user
        url.append("&user=%s" % user.username)
    if problem is not None:
        kwargs['problem'] = problem
        url.append("&problem=%s" % problem.code)
    if contest is not None:
        kwargs['contest'] = contest
        url.append("&problem=%s" % contest.code)
        
    if score_begin != 0:
        kwargs['score__gte'] = score_begin
        url.append("&score_begin=%d" % score_begin)
    
    if score_end != 100:
        kwargs['score__lte'] = score_end
        url.append("&score_end=%d" % score_end)
    
    if current_user is None or current_user.is_superuser is False:
        kwargs['private'] = False
    
    print kwargs
    jobs = Job.objects.filter(**kwargs).order_by('-id')
    paginator = Paginator(jobs, 10)
    
    if reeval:
        for job in jobs:
            job.percent_completed = 0
            job.processing = False
            job.message = 'Waiting'
            job.score = 0
            job.save()
            Test.objects.filter(job = job).delete()
    
    return render_to_response("grader/status.html",
                              {'paginator' : paginator,
                               'page' : paginator.page(page_ind).object_list,
                               'page_ind' : page_ind,
                               'url' : url,
                               'user' : user,
                               'problem' : problem,
                               'accepted' : True if score_begin == 100 else False,
                               'navigation' : {
                                    'main' : 'judge',
                                    'other' : 'status',
                                },
                              },
                              context_instance = RequestContext(request))
    
    
@login_required
def submit (request):
    user = user_auth(request)
        
    if request.method == 'POST':
        form = JobSubmitForm(request.POST)
        if form.is_valid() and 'solution' in request.FILES:
            job = form.save(commit=False)
            if job.contest.started() is False and user.is_staff is False:
                return redirect_to_index("You can't submit, contest dind't start yet.")
            if job.contest.ended() is True:
                return redirect_to_index("You can't submit, contest ended.")
            job.message, job.type, job.date, job.user, job.source_size, job.percent_completed, job.score = 'Waiting', 'O', datetime.datetime.now(), user, request.FILES['solution'].size, 0, 0
            if job.contest.started() is False or job.contest.code == 'none':
                job.private = True
            job.save()
            save_file(dest = os.path.join(JOBS_DIR, "job%d.%s" % (job.id, job.language)), file = request.FILES['solution'])
            
            return HttpResponseRedirect(reverse('webEval.web_eval__core.grader__controller.status') + '?problem=%s&user=%s' % (job.problem.code, user.username))
    else:
        form = JobSubmitForm()
    
    return render_to_response("grader/submit_form.html",
                             {'form' : form,
                              'compilers' : judge_settings.COMPILERS,
                              'problems' : Problem.objects.all(),
                              'navigation' : {
                                  'main' : 'judge',
                                  'other' : 'display-job',
                              }
                             },
                             context_instance=RequestContext(request))
    
def display_all_contests (request):    
    active_or_upcoming_contests = Contest.objects.filter(end_time__gte = datetime.datetime.now()).order_by('-start_time')
    old_contests = Contest.objects.filter(end_time__lt = datetime.datetime.now()).order_by('-end_time')
    
    return render_to_response('grader/display_all_contests.html',
                              {
                                    'active_or_upcoming_contests' : active_or_upcoming_contests,
                                    'old_contests' : old_contests,
                                    'navigation' : {
                                        'main' : 'judge',
                                        'other' : 'display-all-contests'
                                    }
                              },
                              context_instance = RequestContext(request),
                             )
    

def display_contest_registered_users (request, contest_code):
    contest = get_object_or_404(Contest, code = contest_code)
    
    return render_to_response('grader/display_registered_users.html',
                              {
                                    'contest' : contest,
                                    'navigation' : {
                                        'main' : 'judge',
                                        'other' : 'display-job',
                                    }
                              },
                              context_instance = RequestContext(request))

def display_contest_standings (request, contest_code):
    users = User.objects.all()
    contest = get_object_or_404(Contest, code = contest_code)
    score_caches = ScoreCache.objects.filter(contest = contest).order_by('-score')
    return render_to_response('grader/display_standings.html',
                              {
                                    'users' : users,
                                    'contest' : contest,
                                    'score_caches' : score_caches,
                                    'navigation' : {
                                        'main' : 'judge',
                                        'other' : 'display_standings'
                                    }
                              },
                              context_instance = RequestContext(request)
                             )


@login_required
def toogle_contest_registration (request, contest_code):
    user = user_auth(request)
    contest = get_object_or_404(Contest, code = contest_code)
    
    if contest.registration_started is True or contest.registration_ended is False:
        if contest.registered_users.filter(username=user.username):
            contest.registered_users.remove(user)
        else:
            contest.registered_users.add(user)
    return HttpResponseRedirect(reverse('webEval.web_eval__core.grader__controller.display_contest',
                                       kwargs = {'contest_code' : contest.code }
                                      )
                               )
    
    
def display_problems_by_author (request, author_code):
    user = user_auth(request)
    author = get_object_or_404(Author, code = author_code)
    problems = Problem.objects.filter(author = author)
    
    return render_to_response('grader/display_problems_by_author.html',
                              {
                                    'author' : author,
                                    'problems' : problems,
                                    'navigation' : {
                                        'main' : 'judge',
                                        'other' : 'display-problems-by-author'
                                    }
                              },
                              context_instance = RequestContext(request))
    
def get_rounds_for_problem (request):
    problem = get_object_or_None(Problem, id=request.GET['problem_id']) if request.method == 'GET' and 'problem_id' in request.GET else None
    contests = problem.contest_set.filter(start_time__lte = datetime.datetime.now(), end_time__gte = datetime.datetime.now()) if problem is not None else None
    
    return render_to_response('grader/get_rounds_for_problem.html',
                              {'contests' : contests},
                              context_instance = RequestContext(request))


def ranks (request):
    users = UserProfile.objects.all().order_by('-rating')
    return render_to_response('grader/display_ranks.html',
                              {
                                    'users' : users,
                                    'navigation' : {
                                            'main' : 'judge',
                                            'other' : 'display_ranks',
                                    }
                              },
                              context_instance = RequestContext(request)
                             )
    

@login_required
def admin_page (request):
    user = user_auth(request)
    
    if user.is_superuser is False and user.is_staff is False:
        return redirect_to_index("You don't have permission to access this page")
    
    if request.method == 'POST':
        form = TicketMilestoneForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TicketMilestoneForm()
        
    last_users = UserProfile.objects.all().order_by('-id')[:20]
    last_logins = UserProfile.objects.all().order_by('-last_login')[:20]
    
    return render_to_response('grader/admin_page.html',
                              {
                                    'last_users' : last_users,
                                    'last_logins' : last_logins,
                                    'milestones' : TicketMilestone.objects.all().order_by('due'),
                                    'milestone_form' : form,
                                    'navigation': {
                                        'main' : 'admin',
                                        'other' : 'admin_page',
                                    }
                              },
                              context_instance = RequestContext(request)
                             )
