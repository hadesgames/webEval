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
from django.core.urlresolvers import resolve
from django.template import RequestContext, Context
from django.shortcuts import get_object_or_404, render_to_response
from django.views.decorators.csrf import csrf_protect

from webEval.web_eval__core.auth__helper import user_auth
from webEval.web_eval__core.models import *
from webEval.web_eval__core.utils__controller import *

def get_parents (board):
    board_it = board
    stack = [];
    while board_it is not None:
        stack.append(board_it);
        board_it = board_it.parent_board
    return stack

def display_board (request, board_id) :
    board = get_object_or_404(ForumBoard, id = board_id)
    
    board_sons = ForumBoard.objects.filter(parent_board = board).order_by('id')
    topic_sons = ForumTopic.objects.filter(board = board).order_by('-last_post')
    
    return render_to_response('forum/display_board.html',
                             {'board_sons' : board_sons,
                              'topic_sons' : topic_sons,
                              'board_id' : board_id,
                              'board' : board,
                              'stack' : get_parents(board),
                              'topnav_page': 'forum',
                              'navigation' : 
                              {
                                    'main' : 'forum', 
                                    'other' : 'display-board'
                              }
                             },
                             context_instance = RequestContext(request)
                             )
    
    
def display_topic (request, topic_id):
    topic = get_object_or_404(ForumTopic, id = topic_id)
    user = user_auth(request)
    
    topic.views += 1
    topic.save()
    
    return render_to_response('forum/display_topic.html',
                              {'topic' : topic,
                               'stack' : get_parents(topic.board),
                               'posts' : ForumPost.objects.filter(topic=topic),
                               'navigation' : 
                                {
                                    'main' : 'forum', 
                                    'other' : 'display-topic'
                                }
                              },
                              context_instance = RequestContext(request)
                             )


@login_required
def new_topic (request, board_id):
    board = get_object_or_404(ForumBoard, id=board_id)
    user = user_auth(request)
    
    if request.method == 'POST':
        form = ForumTopicCreateForm(request.POST)
        if form.is_valid():
            topic = ForumTopic(board=board, author=user)
            topic.save()
            
            post = ForumPost()
            post.topic = topic
            post.author = user
            post.title = form.data['title']
            post.content = form.data['content']
            post.date = datetime.datetime.now()
            post.save()
            
            topic.first_post = post
            topic.last_post = post
            topic.save()
            
            board_it = topic.board
            while board_it is not None:
                board_it.topics += 1
                board_it.last_post = post
                board_it.save()
                board_it = board_it.parent_board
            
            
            user.forum_posts += 1
            user.save()
            
            return HttpResponseRedirect(reverse('webEval.web_eval__core.forum__controller.display_topic',
                                                kwargs={'topic_id' : topic.id}))
    else:
        form = ForumTopicCreateForm()

    return render_to_response('forum/new_topic.html',
                              {'board' : board,
                               'form' : form,
                               'stack' : get_parents(board),
                               'navigation' : 
                                {
                                    'main' : 'forum', 
                                    'other' : 'new-topic'
                                }
                              },
                              context_instance = RequestContext(request)
                             )
    

@login_required
def edit_post (request, post_id):
    user = user_auth(request)
    post = get_object_or_404(ForumPost, id = post_id)
    
    if post.can_edit(user) is False:
        return redirect_to_index("You don't have permissions to edit this post.")
    
    if request.method == 'POST':
        form = ForumPostEditForm(request.POST, instance = post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("webEval.web_eval__core.forum__controller.display_topic",
                                                kwargs={'topic_id' : post.topic.id }) + "#%d" % post.id)
    else:
        form = ForumPostEditForm(post)
        
    return render_to_response('forum/edit_post.html',
                              {'post' : post,
                               'form' : form,
                               'navigation' : 
                                {
                                    'main' : 'forum', 
                                    'other' : 'edit-post'
                                }
                              },
                              context_instance = RequestContext(request)
                             )


def move_post (request, post_id):
    pass


@login_required
def delete_post (request, post_id):
    user = user_auth(request)
    post = get_object_or_404(ForumPost, id = post_id)
    
    if post.can_delete(user) is False:
        return redirect_to_index("You don't have enough permissions to delete this post.")
    
    topic = post.topic
    topic.posts -= 1
    topic.save()
    
    if post == topic.last_post:
        topic.last_post = ForumPost.objects.filter(topic = topic).order_by('id').reverse()[1]
        topic.save()
    
    board_it = post.topic.board
    while board_it is not None:
        board_it.posts -= 1
        board_it.save()
        if board_it.last_post == post:
            fake_post = ForumPost(id=-1)
            
            for y in ForumTopic.objects.filter(board=board_it):
                if y.last_post is not None and y.last_post != post and y.last_post.id > fake_post.id:
                    fake_post = y.last_post
            for y in ForumBoard.objects.filter(parent_board=board_it):
                if y.last_post is not None and y.last_post != post and y.last_post.id > fake_post.id:
                    fake_post = y.last_post
            board_it.last_post = fake_post
            board_it.save()
        board_it = board_it.parent_board
    
    
    post.author.forum_posts -= 1
    post.author.save()
    
    post.delete()
    
    return HttpResponseRedirect(reverse("webEval.web_eval__core.forum__controller.display_topic",
                                                kwargs={'topic_id' : topic.id }))


@login_required
def reply (request, topic_id):
    user = user_auth(request)
    topic = get_object_or_404(ForumTopic, id = topic_id)
    board = topic.board
    
    if request.method == 'POST':
        form = ForumPostReplyForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.topic = topic
            post.author = user
            post.date = datetime.datetime.now()
            post.save()
            
            post.topic.posts += 1
            post.topic.last_post = post
            post.topic.save()
            
            board_it = post.topic.board
            while board_it is not None:
                board_it.posts += 1
                board_it.last_post = post
                board_it.save()
                board_it = board_it.parent_board
            
            user.forum_posts += 1
            user.save()
            
            return HttpResponseRedirect(reverse('webEval.web_eval__core.forum__controller.display_topic',
                                                kwargs={'topic_id' : topic.id}))
    else:
        form = ForumPostReplyForm()

    return render_to_response('forum/reply.html',
                              {'topic' : topic,
                               'form' : form,
                               'stack' : get_parents(board),
                               'navigation' : 
                                {
                                    'main' : 'forum', 
                                    'other' : 'reply'
                                }
                              },
                              context_instance = RequestContext(request)
                             )
    