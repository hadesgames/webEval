from django.conf import settings
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import models as auth_models
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_models
from django.contrib.auth.models import User
from openid.consumer.consumer import SUCCESS
from django.core.mail import mail_admins

from webEval.web_eval__core.models import *
from webEval.web_eval__core.wiki__helper import *

import cgi
import urllib
import simplejson 

class CustomUserModelBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        dir(self.user_class)
        try:
            user = self.user_class.objects.get(username=username)
            if user.check_password(password):
                return user
        except self.user_class.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return self.user_class.objects.get(pk=user_id)
        except self.user_class.DoesNotExist:
            return None

    @property
    def user_class(self):
        if not hasattr(self, '_user_class'):
            self._user_class = get_model(*settings.CUSTOM_USER_MODEL.split('.', 2))
            if not self._user_class:
                raise ImproperlyConfigured('Could not get custom user model')
        return self._user_class

class FacebookBackend:
    
    def authenticate(self, token=None):

        facebook_session = FacebookSession.objects.get(
            access_token=token,
        )

        profile = facebook_session.query('me')
   
        try:
            user = UserProfile.objects.get(facebook_uid=profile['id'])
        except UserProfile.DoesNotExist, e:
            return None #user = auth_models.User(username=profile['id'])
        
        try:
            FacebookSession.objects.get(uid=profile['id']).delete()
        except FacebookSession.DoesNotExist, e:
            pass

        facebook_session.uid = profile['id']
        facebook_session.user = user
        facebook_session.save()
   
        return user.user_ptr
   
    def get_user(self, user_id):

        try:
            return auth_models.User.objects.get(pk=user_id)
        except auth_models.User.DoesNotExist:
            return None
        
class GoogleBackend:

    def authenticate(self, openid_response):
        if openid_response is None:
            return None
        if openid_response.status != SUCCESS:
            return None
        
        google_email = openid_response.getSigned('http://openid.net/srv/ax/1.0', 'value.email')
        google_firstname = openid_response.getSigned('http://openid.net/srv/ax/1.0', 'value.firstname')
        google_lastname = openid_response.getSigned('http://openid.net/srv/ax/1.0', 'value.lastname')
        try:
            user = User.objects.get(email=google_email)
        except User.DoesNotExist:
            # create a new user, or send a message to admins, etc.
            return None
        
        return user
    
    def get_user(self, user_id):
    
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
        
class TwitterBackend:
    
    def authenticate(selfself, creds):
        if creds is None:
            return None
        if not 'screen_name' in creds:
            return None
        
        twitter_user = creds['screen_name']
        
        try:
            user = UserProfile.objects.get(twitter_user=twitter_user)
        except UserProfile.DoesNotExist:
            return None
        return user.user_ptr
        
    def get_user(self, user_id):
        
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None