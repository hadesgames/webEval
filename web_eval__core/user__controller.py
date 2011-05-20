import os

from django.shortcuts import get_object_or_404, render_to_response
from django.contrib.auth.decorators import login_required
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.template import RequestContext

from webEval.settings import *
from webEval.web_eval__core.models import *
from webEval.web_eval__core.auth__controller import user_auth
from webEval.web_eval__core.utils__controller import *
from webEval.web_eval__core.utils__helper import save_file
from webEval.web_eval__core.wiki__controller import display_revision, edit_page 

# Displays the username profile
def display_user (request, user_name):
    user = user_auth(request)
    user_profile = get_object_or_404(UserProfile, username=user_name)
    
    return display_revision(revision = user_profile.wiki_page.last_revision,
                            user = user,
                            widgets = {
                                'is_user' : True,
                                'user' : user_profile,
                            },
                            context_instance = RequestContext(request),
                           )


# Edit user description wiki page
@login_required
def edit_user_description (request, user_name):
    user = get_object_or_404(UserProfile, username = user_name)
    return edit_page (request, 
                      page_url = user.wiki_page.url, 
                      widgets = {
                            'is_user' : True, 
                            'user' : user ,
                      }
                     )
    
# Display user rating and rating history
def display_user_rating (request, user_name):
    user = get_object_or_404(UserProfile, username = user_name)
    rating_list = RatingCache.objects.filter(user=user).order_by('date', 'id')
    
    return render_to_response('grader/display_user_rating.html',
                              {
                                    'user' : user,
                                    'rating_list' : rating_list,
                                    'rating' : True,
                                    'navigation' : {
                                        'main' : 'judge',
                                        'other' : 'user-rating',
                                    }
                              },
                              context_instance = RequestContext(request)
                             )

# Display user_statistics
def display_user_statistics (request, user_name):
    user = get_object_or_404(UserProfile, username = user_name)
    return render_to_response('display_user_statistics.html',
                              {
                                    'user' : user,
                                    'navigation' : {
                                        'main' : 'judge',
                                        'other' : 'display-user-statistics'
                                    }
                              },
                              context_instance = RequestContext(request)
                             )


# Edit my account
@login_required
def edit_user_account (request, user_name):
    user = user_auth(request)
    username = get_object_or_404(UserProfile, username = user_name)
    
    if user.has_perm('web_eval__core.edit_userprofile') is False and user != username:
        return redirect_to_index("You don't have permission to edit this user.")
    
    if request.method == 'POST':
        form = UserEditAccountForm(request.POST, instance = username)
        
        if 'avatar' in request.FILES:
            print "OKAY"
            dest = os.path.join(AVATARS_DIR, "%s_%s" % (username.username, request.FILES['avatar'].name))
            prefix = os.path.join(AVATARS_DIR, "%s_" % username.username)
            save_file(dest = dest, file = request.FILES['avatar'])
            
            os.system("convert %s %s" % (dest, prefix + "normal.jpeg"))
            os.system("convert %s -resize 150^ -gravity Center -crop 150x150+0+0 +repage %s" % (prefix + "normal.jpeg", prefix + "medium.jpeg"))
            os.system("convert %s -resize 50^ -gravity Center -crop 50x50+0+0 +repage %s" % (prefix + "normal.jpeg", prefix + "small.jpeg"))
            os.system("convert %s -resize 16x16^ -gravity Center -crop 16x16+0+0 +repage %s" % (prefix + "normal.jpeg", prefix + "tiny.jpeg"))
            os.system("convert %s -resize 100 %s" % (prefix + "normal.jpeg", prefix + "100px.jpeg"))
            os.remove(dest)
            
        if form.is_valid ():
            form.save()
            
    else:
        form = UserEditAccountForm(username)
        
    return render_to_response('user_edit_account.html',
                              {'form' : form,
                               'user' : user,
                               'navigation' : {
                                    'main' : 'judge',
                                    'other' : 'edit-account',
                               }
                              },
                              context_instance = RequestContext(request),
                             )
    
    
def get_avatar (request, user_name):
    username = get_object_or_404(User, username = user_name)
    
    filename = os.path.join(AVATARS_DIR, "%s_normal.jpeg" % username.username)
    wrapper = FileWrapper(file(filename))
    response = HttpResponse(wrapper, content_type='image/jpeg')
    response['Content-Length'] = os.path.getsize(filename)
    response['Content-Disposition'] = 'attachment; filename="%s"' % "avatar_%s.jpeg" % username.username
    return response


@login_required
def new_private_message (request):
    user_from = user_auth(request)
    user_to = request.GET['to'] if 'to' in request.GET else None
    user = get_object_or_404(UserProfile, username=user_to) if user_to is not None else None
    
    if request.method == 'POST':
        form = PrivateMessageForm(request.POST)
        if form.is_valid ():
            pm = form.save(commit = False)
            pm.date = datetime.datetime.now()
            pm.user_from = user_from
            pm.save()
            return HttpResponseRedirect(reverse('webEval.web_eval__core.user__controller.private_messages') + '#post%d' % pm.id)
    else:
        form = PrivateMessageForm()
        
    return render_to_response('forum/new_pm.html',
                              {
                                    'user' : user,
                                    'navigation' : {
                                        'main' : 'forum',
                                        'other' : 'new-private-message'
                                    }                                
                              },
                              context_instance = RequestContext(request)
                             )
    

@login_required    
def private_messages (request):
    user = user_auth(request)
    inbox = PrivateMessage.objects.filter(user_to = user).order_by('-id')
    outbox = PrivateMessage.objects.filter(user_from = user).order_by('-id')
    
    return render_to_response('forum/display_private_messages.html',
                              {
                                    'inbox' : inbox,
                                    'outbox' : outbox,
                                    'navigation' : {
                                        'main' : 'forum',
                                        'other' : 'private-messages'
                                    }
                              },
                              context_instance = RequestContext(request),
                             )