import datetime
import re

from django.core.urlresolvers import reverse

from webEval.web_eval__core.auth__helper import user_auth
from webEval.web_eval__core.models import *
from webEval.web_eval__core.utils__helper import get_ip_from_request

def create_problem_wiki_page (problem, request):
    user = user_auth(request)
    
    w = WikiPage()
    w.url = reverse('webEval.web_eval__core.grader__controller.display_problem',
                    kwargs = { 'problem_code' : problem.code }).rstrip('/').lstrip('/')
    w.author = user
    w.save()
    
    r = WikiRevision()
    r.revision_id = 1
    r.content = """
== %s ==
Problem body...
=== Input file ===
From input file //%s.in// ...
=== Output file ===
Write ... to output file //%s.out//.
=== Restrictions and specifications
*0 < //N// < 1000

|=%s.in |=%s.out |
|some input |some output |
                """ % (problem.code, problem.code, problem.code, problem.code, problem.code)
    
    r.date = datetime.datetime.now()
    r.ip = get_ip_from_request(request)
    r.wiki_page = w
    r.title = problem.code
    r.markup_type = 'C'
    r.security = 'Private'
    r.author = user
    r.save()
    
    w.last_revision = r
    w.save()
    
    return w


def create_user_wiki_page (user, request):
    w = WikiPage()
    w.url = reverse('webEval.web_eval__core.user__controller.display_user',
                    kwargs = { 'user_name' : user.username }).rstrip('/').lstrip('/')
    w.author = user
    w.save()
    
    r = WikiRevision()
    r.revision_id = 1
    r.content = """
== About me ==
Write here about you...                 
                """
    r.date = datetime.datetime.now()
    r.ip = get_ip_from_request(request)
    r.wiki_page = w
    r.title = "Profile: %s" % user.username
    r.markup_type = 'C'
    r.security = 'Protected'
    r.author = user
    r.save()
    
    w.last_revision = r
    w.save()
    
    return w


def create_contest_wiki_page (contest, request):
    user = user_auth(request)
    
    w = WikiPage()
    w.url = reverse('webEval.web_eval__core.grader__controller.display_contest',
                    kwargs = {'contest_code' : contest.code }).rstrip('/').lstrip('/')
    w.author = user
    w.save()
    
    r = WikiRevision()
    r.revision_id = 1
    r.content = """ 
=== Contest %s ==
Write here about contest %s...
                """ % (contest.code, contest.code)
    r.date = datetime.datetime.now()
    r.ip = get_ip_from_request(request)
    r.wiki_page = w
    r.title = "Contest %s" % contest.code
    r.markup_type = 'C'
    r.security = 'Private'
    r.author = user
    r.save()
    
    w.last_revision = r
    w.save()
    
    return w


def replace_youtube_link (value):
    reg = '(http://(www\.)?youtube\.com/watch\?v=(?P<youtube_id>[\w-]+)(\&|$)?([^\s\r\n<]*))'
    reg2 = reg.replace('youtube_id', 'youtube_id2')
    match_reg = '<a href="%s">%s</a>' % (reg, reg2)
    replace_reg = '<iframe id="iframe\g<youtube_id>" title="YouTube video player" class="youtube_player" type="text/html" width="425" height="349" src="http://www.youtube.com/embed/\g<youtube_id>?rel=0" frameborder="0" allowFullScreen></iframe>'
    return re.sub(match_reg, replace_reg, value)

def replace_vimeo_link (value):
    reg = '(http://(www\.)?vimeo\.com/(?P<vimeo_id>\d+))'
    reg2 = reg.replace('vimeo_id', 'vimeo_id2')
    match_reg = '<a href="%s">%s</a>' % (reg, reg2)
    replace_reg = '<iframe src="http://player.vimeo.com/video/\g<vimeo_id>?title=0&amp;byline=0&amp;portrait=0" width="560" height="315" frameborder="0"></iframe><p>'
    return re.sub(match_reg, replace_reg, value)

def markup (value):
    value = replace_youtube_link(value)
    value = replace_vimeo_link(value)
    return value
