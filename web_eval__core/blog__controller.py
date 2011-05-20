import datetime
import hashlib
import re

from annoying.functions import get_object_or_None

from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.comments.models import Comment
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import resolve
from django.db.models import Q
from django.template import RequestContext, Context
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.csrf import csrf_protect

from webEval.web_eval__core.auth__helper import user_auth
from webEval.web_eval__core.models import *
from webEval.web_eval__core.utils__controller import redirect_to_index


def index (request, username = None):
    username = get_object_or_None(UserProfile, username = username)
    if username is not None:
        blog_entries = BlogEntry.objects.filter(author=username).order_by('id').reverse()
    else:
        blog_entries = [y.blog_entry for y in DashboardEntry.objects.all().order_by('id').reverse()]
        
    if username is None:
        last_blog_entries = [y.blog_entry for y in DashboardEntry.objects.all().order_by('-id')[:10]]
    else:
        last_blog_entries = BlogEntry.objects.filter(author = username).order_by('-id')[:10]
    
    
    return render_to_response('blog/list_entries.html',
                              {
                                    'blog_entries' : blog_entries,
                                    'blog_title' : 'webEval Dashboard' if username is None else "%s's blog" % username.username,
                                    'last_blog_entries' : last_blog_entries,
                                    'navigation' : 
                                    {
                                        'main' : 'blog', 
                                        'other' : 'display-entries',
                                        'author' : username if username is not None else None,
                                    }  
                              }, 
                              context_instance=RequestContext(request))


@csrf_protect
def display_entry (request, username, permalink):
    user = user_auth(request)
    username = get_object_or_404(UserProfile, username = username)
    blog_entry = get_object_or_404(BlogEntry, author = username, permalink = permalink)
    can_edit = user is not None and (user.has_perm('web_eval__core.edit_blogentry') or user == username)
    can_delete = user is not None and (user.has_perm('web_eval__core.delete_blogentry') or user == username)
    can_manage_dashboard = user is not None and (user.has_perm('web_eval__core.add_dashboardentry'))
    is_dashboard_entry = len(DashboardEntry.objects.filter(blog_entry = blog_entry)) > 0
    
    return render_to_response('blog/display_entry.html', 
                              {'blog_entry' : blog_entry,
                               'can_edit' : can_edit,
                               'can_delete' : can_delete,
                               'can_manage_dashboard' : can_manage_dashboard,
                               'last_blog_entries' : BlogEntry.objects.filter(author = username).order_by('-date')[:10],
                               'is_dashboard_entry' : is_dashboard_entry,
                               'navigation' : 
                               {
                                    'main' : 'blog', 
                                    'other' : 'display-blog-entry',
                                    'author' : blog_entry.author,
                               } 
                              }, 
                              context_instance=RequestContext(request))
    

def update_tags (blog_entry, tags):
    for tag in blog_entry.tags.all():
        tag.uses -= 1
        tag.save()
    blog_entry.tags.clear()
    for tag in tags:
        tag = Tag.objects.get(name = tag) if Tag.objects.filter(name = tag) else Tag(name = tag)
        tag.uses += 1
        tag.save()
        blog_entry.tags.add(tag)
    blog_entry.save()
    
    
@login_required
def new_entry (request):
    user = user_auth(request)
        
    if request.method == 'POST':
        form = BlogEntryCreateForm(request.POST)
        if form.is_valid():
            blog_entry = form.save(commit=False)
            blog_entry.author = user
            blog_entry.date = datetime.datetime.now()
            blog_entry.permalink = hashlib.md5(str(datetime.datetime.now())).hexdigest()
            blog_entry.save()
            
            blog_entry.permalink = blog_entry.get_permalink()
            blog_entry.save()
            return HttpResponseRedirect(reverse("webEval.web_eval__core.blog__controller.display_entry",
                                                kwargs = {'username' : blog_entry.author.username,
                                                          'permalink' : blog_entry.permalink,
                                                         }
                                                )
                                       )
    else:
        form = BlogEntryCreateForm()
    return render_to_response("blog/new_entry.html", 
                              {'form' : form,
                               'navigation' : 
                               {
                                    'main' : 'blog', 
                                    'other' : 'create-blog-post'
                               } 
                              }, 
                              context_instance=RequestContext(request))


@login_required
def edit_entry (request, username, permalink):
    user = user_auth(request)
    username = get_object_or_404(UserProfile, username = username)
    blog_entry = get_object_or_404(BlogEntry, author = username, permalink = permalink)
    
    if user.has_perm('web_eval__core.edit_blogentry') is False and user != username:
        return redirect_to_index("You don't have permission to edit this blog entry.")
    
    if request.method == 'POST':
        form = BlogEntryEditForm(request.POST, instance = blog_entry)
        
        
        if form.is_valid ():
            form.save()
            
            tags = []
            for tag, value in request.POST.iteritems():
                if re.match('tag(?P<tag_name>\d+)input', tag):
                    tags.append(value)
                
            update_tags (blog_entry, tags)
            
            return HttpResponseRedirect(reverse("webEval.web_eval__core.blog__controller.display_entry",
                                                kwargs = {'username' : username.username,
                                                          'permalink' : permalink,
                                                         }
                                                )
                                       )
    else:
        form = BlogEntryEditForm(blog_entry)
        
    return render_to_response('blog/edit_entry.html',
                              {'form' : form,
                               'blog_entry' : blog_entry,
                               'navigation' : {
                                    'main' : 'blog',
                                    'other' : 'edit-entry'
                                }
                              },
                              context_instance=RequestContext(request)
                             )
        
        
        
@login_required
def delete_entry (request, username, permalink):
    user = user_auth(request)
    
    if user.has_perm('web_eval__core.blogentry_delete') is False:
        return redirect_to_index("You don't have permission to delete blog entries.")
    
    username = get_object_or_404(UserProfile, username = username)
    blog_entry = get_object_or_404(BlogEntry, author = username, permalink = permalink)
    blog_entry.delete()
    
    return HttpResponseRedirect(reverse('webEval.web_eval__core.blog__controller.index'))


@login_required
def delete_comment(request, post_pk, pk=None):
    """Delete comment(s) with primary key `pk` or with pks in POST."""
    if request.user.is_staff:
        blog_entry = get_object_or_404(BlogEntry, pk = post_pk)
        if not pk: 
            pklst = request.POST.getlist("delete")
        else:
            pklst = [pk]

        for pk in pklst:
            Comment.objects.get(pk=pk).delete()
        return HttpResponseRedirect(reverse("webEval.web_eval__core.blog__controller.display_entry",
                                            kwargs={'username' : blog_entry.author.username,
                                                    'permalink' : blog_entry.permalink,
                                                   }
                                           ) + "#comments"
                                   )


def get_tags_ajax (request):
    if request.is_ajax():
        q = request.GET.get( 'q' )
        if q is not None:            
            results = Tag.objects.filter(Q(name__contains = q)).order_by( 'name' )
            return render_to_response('blog/tag_search_results.html',
                                      {'results' : results},
                                      context_instance = RequestContext(request),
                                     )


@login_required
def add_tag_ajax (request):
    if request.is_ajax():
        q = request.GET.get('q')
        permalink = request.GET.get('permalink')
        
        if q is not None and permalink is not None:
            entry = get_objects_or_404(BlogEntry, permalink=q)
            tag = get_objects_or_None(Tag, name=q)
            
            if user.has_perm('web_eval__core.edit_blogentry') is False and user != username:
                return HttpResponse("You don't have permission to add tags to this blog entry.")
            
            if tag is None:
                return HttpResponse("Tag does not exist.")
            
            entry.tags.add(tag)
            return HttpResponse("Tag added.")
        
        
def comment_posted (request):
    if 'c' in request.GET:
        comment_id = request.GET['c']
        comment = get_object_or_404(Comment, id=comment_id)
        post_id = comment.object_pk
        post = BlogEntry.objects.get( pk=post_id )

        if post:
            return HttpResponseRedirect(reverse('webEval.web_eval__core.blog__controller.display_entry',
                                                kwargs = {'username' : post.author.username,
                                                          'permalink' : post.permalink
                                                         }
                                               ) + '#comment' + comment_id
                                        )

    return HttpResponseRedirect( "/" )


@login_required
def toogle_dashboard (request, username, permalink):
    user = user_auth(request)
    username = get_object_or_404(UserProfile, username = username)
    blog_entry = get_object_or_404(BlogEntry, author = username, permalink = permalink)
    
    if user.has_perm('web_eval__core_add_dashboardentry') is False:
        return redirect_to_index("You don't have permission to modify dashboard.")
    
    if DashboardEntry.objects.filter(blog_entry = blog_entry):
        DashboardEntry.objects.filter(blog_entry = blog_entry).delete()
    else:
        DashboardEntry(blog_entry = blog_entry).save()
        
    return HttpResponseRedirect(reverse('webEval.web_eval__core.wiki__controller.dashboard'))
        