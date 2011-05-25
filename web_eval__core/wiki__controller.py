import datetime
import difflib
import hashlib
import os

from annoying.functions import get_object_or_None

from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import resolve, reverse
from django.template import RequestContext, Context
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from webEval import judge_settings
from webEval.settings import ATTACHMENTS_DIR
from webEval.utils.diff_match_patch import *
from webEval.web_eval__core.auth__helper import user_auth
from webEval.web_eval__core.blog__controller import index
from webEval.web_eval__core.models import *
from webEval.web_eval__core.permissions__config import *
from webEval.web_eval__core.utils__controller import redirect_to_index, redirect_with_message
from webEval.web_eval__core.utils__helper import get_ip_from_request, save_file


@login_required
def create_wiki_page (request, page_url = None):  
    user = user_auth(request)
    
    if user.has_perm('web_eval__core.add_wikipage') is False:
        return redirect_to_index("You don't have permission to add wiki pages.")
    
    if WikiPage.objects.filter(url = page_url):
        return redirect_to_index("Page already exists...")
    
    if request.method == 'POST':
        form = WikiRevisionEditForm(request.POST)
        
        if form.is_valid():
            page_url = request.POST['url']
            page = WikiPage()
            page.url = page_url
            page.author = user
            page.save()
            
            revision = form.save(commit = False)
            revision.revision_id = 1
            revision.date = datetime.datetime.now()
            revision.ip = get_ip_from_request(request)
            revision.wiki_page = page
            revision.author = user
            revision.save()
            
            page.last_revision = revision
            page.save()
            
            return HttpResponseRedirect(reverse('webEval.web_eval__core.wiki__controller.display_page',
                                            kwargs={'page_url' : page_url }))
    else:
        form = WikiRevisionEditForm()
    
    return render_to_response('wiki_edit_revision.html', 
                              {'revision' : 1,
                               'form' : form,
                               'edit' : False,
                               'page_url' : page_url,
                              },
                              context_instance = RequestContext(request)
                             )
 

@login_required
def edit_page (request, page_url, widgets = {}):
    user = user_auth(request)
    page = get_object_or_404(WikiPage, url=page_url)    
    revisions_list = WikiRevision.objects.filter(wiki_page=page)

    if not page.last_revision.can_edit(user):
        return redirect_to_index("You don't have enough rights to edit this page, i will redirect you...")
    
    if request.method == 'POST':    # we have some POST data.
        form = WikiRevisionEditForm(request.POST)
        if form.is_valid():
            revision = form.save(commit = False)
            revision.revision_id = page.last_revision.revision_id + 1
            revision.date = datetime.datetime.now()
            revision.ip = get_ip_from_request(request)
            revision.wiki_page = page
            revision.author = user
            revision.save()
            
            page.last_revision = revision
            page.save()
            if 'is_problem' in widgets:
                return HttpResponseRedirect(reverse('webEval.web_eval__core.grader__controller.display_problem',
                                                    kwargs = {'problem_code' : widgets['problem'].code }))
                
            return HttpResponseRedirect(reverse('webEval.web_eval__core.wiki__controller.display_page',
                                                    kwargs = {'page_url' : page.url }))
        else:
            print form.errors
    else:    
        form = WikiRevisionEditForm(page.last_revision)
        
    can_attach = page.last_revision.wiki_page.can_attach_files(user)
    can_edit = page.last_revision.can_edit(user)
    can_view = page.last_revision.can_view(user)
    
    return render_to_response('wiki_edit_revision.html', 
                              {'revision' : page.last_revision,
                               'page' : page,
                               'form' : form,
                               'edit' : True,
                               'widgets' : widgets,
                               'can_view' : can_view,
                               'can_edit' : can_edit,
                               'can_attach' : can_attach,
                               'navigation' : {
                                    'main' : 'wiki',
                                    'other' : 'edit-page',
                               }
                              },
                              context_instance = RequestContext(request)
                             )

# Shows the history of page
def history (request, page_url, widgets = {}):
    user = user_auth(request)
    page = get_object_or_404(WikiPage, url = page_url)
    revisions = WikiRevision.objects.filter(wiki_page = page).order_by('-revision_id')
    
    if page.last_revision.can_view(user) is False:
        return redirect_to_index("You don't have enough rights to view this page's history")
    
    problem = get_object_or_None(Problem, wiki_page=page)
    if problem is not None:
        widgets['is_problem'] = True
        widgets['problem'] = problem
        
    user_profile = get_object_or_None(UserProfile, wiki_page=page)
    if user_profile is not None:
        widgets['is_user'] = True
        widgets['user'] = user_profile
        
    can_attach = page.last_revision.wiki_page.can_attach_files(user)
    can_edit = page.last_revision.can_edit(user)
    can_view = page.last_revision.can_view(user)
        
    return render_to_response('wiki_display_history.html',
                              {
                               'page' : page,
                               'revisions' : revisions,
                               'widgets' : widgets,
                               'can_view' : can_view,
                               'can_edit' : can_edit,
                               'can_attach' : can_attach,
                               'navigation' : {
                                    'main' : 'wiki',
                                    'other' : 'history',
                                }
                              },
                              context_instance = RequestContext(request))
    
# Diff between two revisions
def diff (request, page_url):
    if request.method != 'GET' or 'r1' not in request.GET or 'r2' not in request.GET:
        raise Http404
    page = get_object_or_404(WikiPage, url = page_url)
    r1 = get_object_or_404(WikiRevision, revision_id=request.GET['r1'])
    r2 = get_object_or_404(WikiRevision, revision_id=request.GET['r2'])
    diff = diff_match_patch()
    
    return render_to_response('wiki_diff_revisions.html',
                              {
                               'r1' : r1,
                               'r2' : r2,
                               'diff' : diff.diff_prettyHtml(diff.diff_main(r1.content, r2.content))
                              },
                              context_instance = RequestContext(request))

# attach files to a page
@login_required
def attach (request, page_url):
    user = user_auth(request)
    page = get_object_or_404(WikiPage, url = page_url)
    
    if page.can_attach_files(user) is False:
        return redirect_to_index("You don't have permissions to attach files to this page.")
    
    message = None

    if request.method == 'POST':
        if 'file_name' in request.FILES:
            attachment = WikiAttachment()
            attachment.name = request.FILES['file_name'].name
            attachment.wiki_page = page
            attachment.ip = get_ip_from_request(request)
            attachment.size = request.FILES['file_name'].size
            attachment.date = datetime.datetime.now()
            attachment.author = user
            attachment.security = 'Public'
            attachment.hash = ''
            attachment.save()
            
            attachment.hash = hashlib.md5(str(attachment.id)).hexdigest()
            attachment.save()
            
            save_file(dest = os.path.join(ATTACHMENTS_DIR, "attachment%d-%s" % (attachment.id, attachment.name)), file = request.FILES['file_name'])
            
            message = 'File uploaded successfully.'
        
    can_attach = page.last_revision.wiki_page.can_attach_files(user)
    can_edit = page.last_revision.can_edit(user)
    can_view = page.last_revision.can_view(user)
        
    return render_to_response('wiki/attach.html',
                              {
                               'page' : page,
                               'message' : message if message is not None else '',
                               'can_view' : can_view,
                               'can_edit' : can_edit,
                               'can_attach' : can_attach,
                               'navigation' : {
                                    'main' : 'wiki',
                                    'other' : 'attach',
                               }
                              },
                              context_instance = RequestContext(request),
                             )

# Show attachments of a page
@login_required
def attachments (request, page_url):
    user = user_auth(request)
    page = get_object_or_404(WikiPage, url = page_url)
    attachments = WikiAttachment.objects.filter(wiki_page=page)
    
    can_attach = page.last_revision.wiki_page.can_attach_files(user)
    can_edit = page.last_revision.can_edit(user)
    can_view = page.last_revision.can_view(user)
    
    return render_to_response('wiki/attachments.html',
                              {
                               'page' : page,
                               'attachments' : attachments,
                               'can_view' : can_view,
                               'can_edit' : can_edit,
                               'can_attach' : can_attach,
                               'navigation' : {
                                    'main' : 'wiki',
                                    'other' : 'attachments',
                               }
                              },
                              context_instance = RequestContext(request),
                             )
    

# display attachment
@login_required
def display_attachment (request, page_url, hash):
    user = user_auth(request)
    wiki_page = get_object_or_404(WikiPage, url = page_url)
    attachment = get_object_or_404(WikiAttachment, wiki_page = wiki_page, hash = hash)
    
    if attachment.can_view(user) is False:
        return redirect_to_index("You don't have enough permissions to view this attachment.")
    
    filename = os.path.join(ATTACHMENTS_DIR, "attachment%d-%s" % (attachment.id, attachment.name))
    try:
      wrapper = FileWrapper(file(filename))
    except IOError:
      raise Http404
    response = HttpResponse(wrapper, content_type='text/plain')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename="%s"' % attachment.name.replace('"', '')
    return response


# rename attachment
@login_required
def rename_attachment (request, page_url, hash):
    pass


# delete attachment
@login_required
@csrf_exempt
def delete_attachment (request, page_url, hash):
    user = user_auth(request)
    wiki_page = get_object_or_404(WikiPage, url = page_url)
    attachment = get_object_or_404(WikiAttachment, wiki_page = wiki_page, hash = hash)
    
    if attachment.can_delete(user) is False:
        return redirect_to_index("You don't have enough permissions to delete this attachment.")
    
    os.remove(os.path.join(ATTACHMENTS_DIR, "attachment%d-%s" % (attachment.id, attachment.name)))
    attachment.delete()
    
    return HttpResponseRedirect(reverse('webEval.web_eval__core.wiki__controller.attachments',
                                        kwargs={'page_url' : wiki_page.url }))

# copy a wiki page   
def copy_page (request, page_url):
    pass
    
# move a wiki page   
def move_page (request, page_url):
    pass

# restore a wiki page to some revision
def restore (request, page_url, revision_id):
    pass

# Displays a revision
def display_revision (revision, user, context_instance, widgets = {}):
    # Find if user cand view or manage (edit, copy, delete, etc) this page
    can_attach = revision.wiki_page.can_attach_files(user)
    can_edit = revision.can_edit(user)
    can_view = revision.can_view(user)
    
    if can_view is False:    # He can't view this page. Let's find why.
        if user is not None:    # He is an user with not enough rights
            return redirect_to_index("You don't have enough rights to view this page")
        else:       # He is not logged in, so we don't know if he can or not view this page, we'll redirect him to login page
            return redirect_with_message(page = reverse('webEval.web_eval__core.auth__controller.login'),
                                         message = "Please login to view this page")
    
    # Finally display the wiki revision
    return render_to_response('wiki_display_revision.html',
                              {'revision' : revision,
                               'can_edit' : can_edit,
                               'can_attach' : can_attach,
                               'widgets' : widgets,
                               'navigation' : {
                                    'main' : 'wiki' if widgets == {} else 'judge',
                                    'other' : 'edit-page',
                               }
                              },
                              context_instance=context_instance)


# Displays a page, either by revision or last revision.
def display_page (request, page_url, revision_id = None, widgets = {}):
    page = get_object_or_None(WikiPage, url = page_url)
    
    if page is None:
        return create_wiki_page(request, page_url)
        
    if revision_id is None:    # Viewing the last revision of page
        revision = page.last_revision
    else:   # Getting revision by revision_id or none
        revision = get_object_or_404(WikiRevision, wiki_page = page, revision_id = revision_id)
        
    # get the current user    
    user = user_auth(request)
    
    return display_revision(revision = revision, 
                            user = user,
                            widgets = widgets, 
                            context_instance = RequestContext(request),
                           )
    
# Download attachments
@login_required
def download_attachments (request, page_url):
    pass

   
def dashboard (request):
    return index(request)


def wiki_index (request):
    last_revisions = WikiRevision.objects.all().order_by('id').reverse()[:10]
    
    return render_to_response('wiki/index.html',
                              {
                                    'last_revisions' : last_revisions,
                                    'navigation' : {
                                        'main' : 'wiki',
                                        'other' : 'wiki-index',
                                    }
                              },
                              context_instance = RequestContext(request))
