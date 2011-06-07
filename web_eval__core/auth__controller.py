import string
import random
import datetime
import cgi
import simplejson
import urllib
import httplib
import time

from urlparse import urlparse

from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import get_object_or_404, render_to_response
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse, resolve
from django.core.mail import EmailMessage
from django.core.exceptions import PermissionDenied
from django.template import RequestContext, Context
#from facebook import Facebook

       
from webEval import settings
from webEval.utils import oauth
from webEval.utils.twitter_utils import *
from webEval.web_eval__core.auth__helper import user_auth, email_is_valid
from webEval.web_eval__core.fields import COUNTRIES
from webEval.web_eval__core.email__helper import send_validation_key
from webEval.web_eval__core.models import *
from webEval.web_eval__core.utils__controller import *
from webEval.web_eval__core.utils__helper import *
from webEval.web_eval__core.wiki__helper import *

CONSUMER = oauth.OAuthConsumer(CONSUMER_KEY, CONSUMER_SECRET)
CONNECTION = httplib.HTTPSConnection(SERVER)

@login_required
def successful_login (request):
    return HttpResponseRedirect(reverse('webEval.web_eval__core.blog__controller.index'))
    
    
def login (request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('webEval.web_eval__core.auth__controller.successful_login'))
            else:
                form.errors['username'] = "Your account has been disabled!"
        else:
            form.errors['username'] = "Your username and password were incorrect."
    else:
        form = UserLoginForm()
        
    return render_to_response('auth/login.html', 
                              {'form' : form, 
                               'settings': settings,
                               'navigation' : {
                                    'main' : 'judge',
                                    'other' : 'login',
                               }
                              },
                              context_instance=RequestContext(request)
                             )
    
def facebook_login (request):
    error = None

    if request.GET:
        if 'code' in request.GET:
            args = {
                'client_id': settings.FACEBOOK_APP_ID,
                'redirect_uri': settings.FACEBOOK_REDIRECT_URI,
                'client_secret': settings.FACEBOOK_API_SECRET,
                'code': request.GET['code'],
            }

            url = 'https://graph.facebook.com/oauth/access_token?' + \
                    urllib.urlencode(args)
            response = cgi.parse_qs(urllib.urlopen(url).read())
            access_token = response['access_token'][0]
            expires = response['expires'][0]

            facebook_session = FacebookSession.objects.get_or_create(
                access_token=access_token,
            )[0]

            facebook_session.expires = expires
            facebook_session.save()

            user = auth.authenticate(token=access_token)
            if user:
                if user.is_active:
                    auth_login(request, user)
                    return HttpResponseRedirect(reverse('webEval.web_eval__core.auth__controller.successful_login'))
                else:
                    error = 'AUTH_DISABLED'
            else:
                error = 'AUTH_FAILED'
        elif 'error_reason' in request.GET:
            error = 'AUTH_DENIED'

    template_context = {'settings': settings, 'error': error}
    return render_to_response('auth/login.html',
                              template_context, 
                              context_instance=RequestContext(request))

def twitter_login (request):
    token = get_unauthorised_request_token(CONSUMER, CONNECTION)
    auth_url = get_authorisation_url(CONSUMER, token)
    response = HttpResponseRedirect(auth_url)
    request.session['unauthed_token'] = token.to_string()
    return response

def twitter_return(request):
    error = None
    unauthed_token = request.session.get('unauthed_token', None)
    print unauthed_token
    if not unauthed_token:
        return HttpResponse("No un-authed token cookie")
    token = oauth.OAuthToken.from_string(unauthed_token)   
    if token.key != request.GET.get('oauth_token', 'no-token'):
        return HttpResponse("Something went wrong! Tokens do not match")
    access_token = exchange_request_token_for_access_token(CONSUMER, CONNECTION, token)   
    auth_key = is_authenticated(CONSUMER, CONNECTION, access_token)
    
    if auth:
        user = auth.authenticate(creds = simplejson.loads(auth_key))
        if user:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('webEval.web_eval__core.auth__controller.successful_login'))
            else:
                error = 'AUTH_DISABLED'
        else:
            error = 'AUTH_FAILED'
    template_context = {'settings': settings, 'error': error}
    return render_to_response('auth/login.html',
                              template_context, 
                              context_instance=RequestContext(request))


def register_remote_form (request):
    form = UserRegisterForm()
    return render_to_response('auth/register_popup.html',
                              {
                               'form' : form,
                               'COUNTRIES' : COUNTRIES,
                               'navigation' : {
                                    'main' : 'judge',
                                    'other' : 'register',
                               }
                              },
                              context_instance = RequestContext(request))
                              
                              
def login_remote_form (request):
    form = UserLoginForm()
    return render_to_response('auth/login_popup.html',
                              {
                                    'form' : form,
                                    'settings' : settings,
                              },
                              context_instance = RequestContext(request)
                             )
    
def register (request):
    messages = []
    if request.POST:
        form = UserRegisterForm(request.POST)#, remote_ip=get_ip_from_request(request))
        
        if form.is_valid():
            username = form.save(commit = False)                                                                   
            username.is_active= 0                                                                                  
            username.date_joined = datetime.datetime.now()                                                         
            username.username = request.POST['username']                                                           
            username.email = request.POST['email']                                                                 
            username.first_name = request.POST['first_name']                                                       
            username.last_name = request.POST['last_name']                                                         
            username.set_password(request.POST['password'])                                                        
            username.save()                                                                                        
            username.wiki_page = create_user_wiki_page(username, request)                                          
            username.save()                                                                                        
            copy_initial_avatar(username)                                                                          
            send_validation_key(username, key = UserValidationKey())                                               
                                                                                                                   
            return HttpResponseRedirect(reverse('webEval.web_eval__core.auth__controller.successful_register'))    
    else:    
        form = UserRegisterForm()
        
    return render_to_response('auth/register.html',
                              {
                               'form' : form,
                               'COUNTRIES' : COUNTRIES,
                               'navigation' : {
                                    'main' : 'judge',
                                    'other' : 'register',
                               }
                              },
                              context_instance = RequestContext(request))
    

def successful_register (request):
    return render_to_response('auth/successful_register.html',
                              {'message' : "An email has been sent to this email adress, please follow the message in the email."},
                              context_instance = RequestContext(request))   

def logout (request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('webEval.web_eval__core.blog__controller.index'))
    

def validate_user (request, user_name, validation_key):
        
    username = get_object_or_404(User, username=user_name).userprofile
    key = get_object_or_404(UserValidationKey, key=validation_key, username = username)
    if datetime.datetime.now() <= key.expire_date:
        key.delete()
        username.is_active = True
        username.save()   
        message = "Your username has been validated, now you can login."
        error = False
    else:
        message = "Your validation key does not exist, or has expired"
        error = True
    return render_to_response('auth/validate_user.html',
                              {'message' : message,
                               'error' : error,
                              },
                              context_instance = RequestContext(request))
