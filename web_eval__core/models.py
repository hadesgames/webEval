import os
import string
import re

from django import forms
from django.db import models
from django.core.validators import email_re
from django.contrib.auth.models import User, UserManager
from django.contrib.comments.signals import comment_was_posted
from django.template.defaultfilters import slugify

#from captcha.fields import CaptchaField

#from webEval.utils.reCaptcha import *

from webEval import judge_settings

from webEval.settings import JOBS_DIR

from webEval.web_eval__core.fields import CountryField, ReCaptchaField
from webEval.web_eval__core.permissions__config import *
from webEval.web_eval__core.widgets import *

################## BLOG ########################
class BlogEntry (models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    author = models.ForeignKey("UserProfile")
    permalink = models.CharField(max_length=255, unique=True)
    date = models.DateTimeField()
    tags = models.ManyToManyField("Tag")
    
    def __unicode__ (self):
        return self.title
    
    def get_permalink (self): # do not call this before save
        return "%s-%d" % (slugify(self.title), self.id)
        
    
class BlogRollEntry (models.Model):
    user = models.ForeignKey('UserProfile')
    link = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=32)
    
    def __unicode__ (self):
        return "%s: %s" % (self.user.username, self.name)
    
    
class DashboardEntry (models.Model):
    blog_entry = models.ForeignKey(BlogEntry)


class Tag (models.Model):
    name = models.CharField(max_length=64)
    uses = models.IntegerField(default = 0)
    
    def __unicode__(self):
        return self.name
    
    def get_uses (self):
        return len(self.blogentry_set.all())
################## FORUM #######################
class ForumBoard (models.Model):
    parent_board = models.ForeignKey("ForumBoard", null = True, blank = True)
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=128, blank=True)
    
    topics = models.IntegerField(default=0)
    posts = models.IntegerField(default=0)
    last_post = models.ForeignKey("ForumPost", null = True, blank = True)
    public = models.BooleanField()
    
    def __unicode__ (self):
        return self.name
    
    def display_sections (self):
        return ', '.join([section.name for section in self.forumboard_set.all()])
    
    
class ForumTopic (models.Model):
    board = models.ForeignKey(ForumBoard)
    author = models.ForeignKey("UserProfile")
    first_post = models.ForeignKey("ForumPost", related_name = 'first_post', null = True, blank = True)
    last_post = models.ForeignKey("ForumPost", related_name = 'last_post', null = True, blank = True)
    
    views = models.IntegerField(default=0)
    posts = models.IntegerField(default=0)
    
    def __unicode__ (self):
        return "Topic: %d" % self.id


class ForumPost (models.Model):
    topic = models.ForeignKey(ForumTopic)
    author = models.ForeignKey("UserProfile")
    
    title = models.CharField(max_length=128)
    content = models.TextField()
    date = models.DateTimeField()
    
    def __unicode__ (self):
        return "Post: %d" % self.id

    def can_edit (self, user):
        return user is not None and (user.has_perm(FORUM_POST_EDIT_ALL) or user == self.author)
    
    def can_delete (self, user):
        return user is not None and (user.has_perm(FORUM_POST_DELETE_ALL) or (user == self.author and self == self.topic.last_post))
    
    def can_move (self, user):
        return user is not None and user.has_perm(FORUM_POST_MOVE)
    

class CalendarEntry (models.Model):
    date = models.DateTimeField()
    title = models.CharField(max_length=64)
    forum_topic = models.ForeignKey(ForumTopic, null=True)
    
    def __unicode__ (self):
        return self.title
    
    
class PrivateMessage (models.Model):
    date = models.DateTimeField()
    user_from = models.ForeignKey("UserProfile", related_name="user_from")
    user_to = models.ForeignKey("UserProfile", related_name="user_to")
    title = models.CharField(max_length=128)
    content = models.TextField()
    
    def __unicode__ (self):
        return "%d" % self.id
    
    
################## GRADER ######################
class Author (models.Model):
    name = models.CharField(max_length=64, unique=True)
    code = models.CharField(max_length=64, unique=True)
    
    def __unicode__ (self):
        return self.name
    

class Contest (models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=16, unique=True)
    
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    wiki_page = models.ForeignKey("WikiPage")
    type = models.CharField(max_length=1, choices=(('A', 'ACM'), ('O', 'Olympiad'), ('C', 'Custom')), default = 'C')
    
    with_rating = models.BooleanField()
    with_open_eval = models.BooleanField()
    
    problems = models.ManyToManyField("Problem")
    registered_users = models.ManyToManyField("UserProfile")
    
    def __unicode__ (self):
        return self.code
    
    def started (self):
        return self.start_time <= datetime.datetime.now()
    
    def ended (self):
        return self.end_time < datetime.datetime.now()
    
    def registered_users_all (self):
        return self.registered_users.all().order_by('-rating')
    
    def registered_users_count (self):
        return len(self.registered_users.all())

    def duration (self):
        return self.end_time - self.start_time
    
    def registration_start_time (self):
        return self.start_time - judge_settings.REGISTRATION_START_TIME
    
    def registration_end_time (self):
        return self.start_time - judge_settings.REGISTRATION_END_TIME
    
    def registration_started (self):
        return datetime.datetime.now() > self.registration_start_time()
    
    def registration_ended (self):
        return datetime.datetime.now() > self.registration_end_time()
    
    
class Problem (models.Model):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=16, unique=True)
    
    owner = models.ForeignKey("UserProfile")
    resource = models.ForeignKey(Contest)
    author = models.ForeignKey(Author)
    
    time_limit = models.IntegerField()
    memory_limit = models.IntegerField()
    source_limit = models.IntegerField()
    
    forum_topic = models.ForeignKey(ForumTopic, null = True, blank = True)
    type = models.CharField(max_length=16, default='Normal')
    wiki_page = models.ForeignKey("WikiPage")
    tags = models.ManyToManyField(Tag)
    
    def __unicode__ (self):
        return self.name

    def can_view (self, user):
        return self.wiki_page.last_revision.can_view(user)

    def get_contests (self):
        return self.contest_set.filter(start_time__lte = datetime.datetime.now(), end_time__gte = datetime.datetime.now())


class Job (models.Model):
    problem = models.ForeignKey(Problem)
    contest = models.ForeignKey(Contest)
    user = models.ForeignKey("UserProfile")
    date = models.DateTimeField()
    message = models.CharField(max_length=32)
    type = models.CharField(max_length=16, choices=(('A', 'ACM'), ('O', 'Olympiad'), ('C', 'Custom')))
    
    percent_completed = models.IntegerField()
    processing = models.BooleanField()
    
    score = models.IntegerField()    
    language = models.CharField(max_length=4, default = 'cpp')
    source_size = models.IntegerField(default=0)
    private = models.BooleanField()
    
    def __unicode__ (self):
        return "%d-%s" % (self.id, self.message)
        
    # TODO
    def can_view (self, user):
        return True
    
    # TODO
    def can_view_source_code (self, user):
        return True
    
    # Transforms bytes in kbytes
    def source_size_in_kbytes (self):
        return 1.00 * self.source_size / 1024
    
    # Returns source code
    def source_code (self):
        source_code = "".join([line for line in open(os.path.join(JOBS_DIR, 'job%s.%s' % (self.id, self.language)))])
        return source_code#.replace('&', '&#38;')#.replace('<', '&#60;').replace('>', '&#62;')


class Test (models.Model):
    job = models.ForeignKey(Job)
    no = models.IntegerField()
    message = models.CharField(max_length=64)
    score = models.IntegerField()
    memory = models.IntegerField(default = 0)
    time = models.IntegerField(default = 0)
    
    def __unicode__ (self):
        return "job %d : test %d" % (self.job.id, self.id)


class GraderTest (models.Model):
    no = models.IntegerField()
    problem = models.ForeignKey(Problem)
    time = models.IntegerField(default = 1000)
    memory = models.IntegerField(default = 16384)
    group = models.IntegerField(default = 1)
    input_size = models.IntegerField(default = 0)
    output_size = models.IntegerField(default = 0)
    feedback = models.BooleanField(default = False)
    
    def __unicode__ (self):
        return "problem %s : test %d" % (self.problem.code, self.no)
    

class RatingCache (models.Model):
    rating = models.IntegerField()
    contest = models.ForeignKey(Contest)
    user = models.ForeignKey("UserProfile")
    date = models.DateTimeField()
    
    def __unicode__ (self):
        return "user: %s, rating: %s" % (self.user.username, self.rating)
    

class ScoreCache (models.Model):
    contest = models.ForeignKey(Contest)
    user = models.ForeignKey("UserProfile")
    score = models.IntegerField(default = 0)
    
    def __unicode__ (self):
        return "%s: %s (%s)" % (self.contest.code, self.user.username, self.score)
    
    def build (self):
        self.score = 0
        for problem in self.scoreproblemcache_set.all():
            self.score += problem.score
        self.save()
    
    
class ScoreProblemCache (models.Model):
    problem = models.ForeignKey(Problem)
    cache = models.ForeignKey(ScoreCache)
    score = models.IntegerField(default = 0)
    
    def __unicode__ (self):
        return "%s: %s (%s)" % (self.problem.code, self.cache.user.username, self.score)
    
    
################## USER #####################
class UserProfile(User):
    avatar = models.ImageField(upload_to='avatars')
    wiki_page = models.ForeignKey("WikiPage", null=True)
    country = CountryField()
    city = models.CharField(max_length=32)
    rating = models.IntegerField(default = 0)
    
    facebook_uid = models.CharField(max_length=16, blank = True, null = True)
    #openid = models.CharField(max_length=64, blank = True, null = True)
    twitter_user = models.CharField(max_length=64, blank = True, null = True)
    
    reputation = models.IntegerField(default = 0)
    forum_posts = models.IntegerField(default = 0)
    
    developer = models.BooleanField(default = False)
    
    objects = UserManager()
    
    def __unicode__(self):
        return self.username
    
    def ip_joined (self):
        return self.wiki_page.wikirevision_set.all()[0].ip
    
    def valid_username (self):
        for char in self.username:
            if char not in string.digits and char not in string.letters and char is not '.' and char is not '_':
                return False
        return True
    

class UserValidationKey(models.Model):
    key = models.CharField(max_length=32)
    username = models.ForeignKey(UserProfile)
    expire_date = models.DateTimeField()
    
    
################### WIKI ##########################
class WikiPage (models.Model):
    author = models.ForeignKey(UserProfile)
    url = models.CharField(max_length=128, unique=True, blank = True)
    last_revision = models.ForeignKey("WikiRevision", default = None, null = True, blank = True)
    
    def __unicode__ (self):
        return self.url
    
    # This function checks if this user can attach files to this page
    # He can attach files if the wikipage is public, he owns it, or he has permission
    def can_attach_files (self, user):
        return user is not None and ((user.has_perm(WIKI_ATTACH_OWN) and user == self.author ) or
                                     (user.has_perm(WIKI_ATTACH_ALL)))
    

class WikiRevision (models.Model):
    revision_id = models.IntegerField()
    content = models.TextField()
    date = models.DateTimeField("date_posted")
    ip = models.IPAddressField()
    
    wiki_page = models.ForeignKey(WikiPage)
    
    markup_type = models.CharField(max_length=1)
    title = models.CharField(max_length=64)
    security = models.CharField(max_length=16)
    author = models.ForeignKey(UserProfile)
    
    
    def __unicode__ (self):
        return "%s: revision %d" % (self.wiki_page.url, self.revision_id)

    # This function checks if this user can view this wiki revision
    # He can view it if it's not private or if he's admin or author

    def can_view (self, user):
        return (self.security != 'Private') or (user is not None and
                                               (user.has_perm(WIKI_VIEW_ALL) or
                                                user == self.wiki_page.author))

    # This function checks if this user can edit this wiki revision
    # He can manage it if it's public or he's author or admin. He must be logged in user.

    def can_edit (self, user):
        return user is not None and (self.security == 'Public' or
                                     user.has_perm(WIKI_EDIT_ALL) or
                                     user == self.wiki_page.author)
                
    # FIXME: decide to allow deleting wiki pages or not.
    """
    def can_delete(self, this_user):
        return this_user and (this_user.has_perm(WIKI_DELETE_ALL) or
                              this_user.has_perm(WIKI_DELETE_OWN) and
                              this_user == self.wiki_page.author)
    """
    
    
class WikiAttachment (models.Model):
    name = models.CharField(max_length = 64)
    wiki_page = models.ForeignKey(WikiPage)
    ip = models.IPAddressField()
    size = models.IntegerField()
    date = models.DateTimeField()
    author = models.ForeignKey(User)
    hash = models.CharField(max_length = 32)
    security = models.CharField(max_length = 16)
    
    def __unicode__ (self):
        return "%s: %s" % (self.wiki_page.url, self.name)
    
    def can_view (self, user):
        return (self.security != 'Private') or (user is not None and
                                               (user.has_perm(WIKI_VIEW_ATTACHMENT_ALL) or
                                                user == self.wiki_page.owner))
    
    def can_edit (self, user):
        return user is not None and (self.security == 'Public' or
                                     user.has_perm(WIKI_EDIT_ATTACHMENT_ALL) or
                                     user == self.wiki_page.owner)
    
    def can_delete (self, user):
        return user is not None and (self.security == 'Public' or
                                     user.has_perm(WIKI_DELETE_ATTACHMENT_ALL) or
                                     user == self.wiki_page.owner)
    

##################################### Tickets: ##############################3#####

class TicketMilestone (models.Model):
    name = models.CharField(max_length = 64, unique = True)
    version = models.FloatField(unique = True)
    due = models.DateField()
    
    def __unicode__ (self):
        return "Milestone: %s" % self.name
    
    def percent_completed (self):
        all_tickets_no = len(self.ticket_set.all())
        completed_tickets_no = len(self.ticket_set.filter(status='completed'))
        return 100 * completed_tickets_no / all_tickets_no if all_tickets_no else 100
    
    def percent_uncompleted (self):
        return 100 - self.percent_completed() 
        

class Ticket (models.Model):
    date_posted = models.DateTimeField()
    title = models.CharField(max_length = 64)
    content = models.TextField()
    type = models.CharField(max_length = 16)
    status = models.CharField(max_length = 16)
    severity = models.CharField(max_length = 16)
    milestone = models.ForeignKey(TicketMilestone, null = True, blank = True)
    author = models.ForeignKey(UserProfile)
    assignee = models.ForeignKey(UserProfile, related_name = "assignee", default = None, null = True, blank = True)
    
    def __unicode__ (self):
        return "Ticket: #%s - %s" % (self.id, self.title)
      

class TicketComment (models.Model):
    date_posted = models.DateTimeField()
    author = models.ForeignKey(UserProfile)
    content = models.TextField()
    ticket = models.ForeignKey(Ticket)
    autogenerated = models.BooleanField(default = False)
    
    def __unicode__ (self):
        return "ticket-comment: %s" % self.id
    
    def can_be_edited (self):
        return self.date_posted + judge_settings.TICKET_COMMENT_EDIT_TIMESTAMP > datetime.datetime.now() and self.autogenerated is False

    
################################# Forms ########################

class BlogEntryCreateForm (forms.ModelForm):
    class Meta:
        model = BlogEntry
        exclude = ('permalink', 'author', 'date', 'tags')


class BlogEntryEditForm (forms.ModelForm):
    class Meta:
        model = BlogEntry
        exclude = ('permalink', 'author', 'date', 'tags')
        

class ContestCreateForm (forms.ModelForm):
    class Meta:
        model = Contest
        exclude = ('start_time', 'end_time', 'name', 'wiki_page', 'with_rating', 'with_open_eval', 'problems', 'registered_users')
        

class ContestEditForm (forms.ModelForm):
    #formfield_callback=parsefield_callback
    class Meta:
        model = Contest
        exclude = ('wiki_page', 'problems', 'registered_users')
        #widgets = {
        #    'start_time' : forms.DateTimeInput(),
        #    'end_time' : forms.DateTimeInput(),
        #}
        

class ForumTopicCreateForm (forms.Form):
    title = models.CharField(max_length=128)
    content = models.TextField()
    

class ForumPostEditForm (forms.ModelForm):
    class Meta:
        model = ForumPost
        exclude = ('topic', 'author', 'date')
    
    
class PrivateMessageForm (forms.ModelForm):
    class Meta:
        model = PrivateMessage
        exclude = ('date', 'user_from')    
        
class ForumPostReplyForm (forms.ModelForm):
    class Meta:
        model = ForumPost
        exclude = ('topic', 'author', 'date')


class JobSubmitForm (forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('percent_completed', 'processing', 'message', 'type', 'date', 'source_size', 'user', 'score', 'private')
        
        
class ProblemCreateForm (forms.ModelForm):
    class Meta:
        model = Problem
        exclude = ('name', 'owner', 'resource', 'author', 'type',
                   'time_limit', 'memory_limit', 'source_limit',
                   'forum_topic', 'wiki_page',  'type', 'tags')
        

class ProblemEditForm (forms.ModelForm):
    class Meta:
        model = Problem
        exclude = ('wiki_page', 'forum_topic', 'type', 'author', 'owner', 'tags')


class TicketForm (forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ('severity', 'status', 'author', 'assignee', 'date_posted')
    

class TicketAdminForm (forms.ModelForm):
    class Meta:
        model = Ticket
        exclude = ('author', 'date_posted')
        

class TicketCommentForm (forms.ModelForm):
    class Meta:
        model = TicketComment
        exclude = ('author', 'date_posted', 'ticket', 'autogenerated')
        
        
class TicketMilestoneForm (forms.ModelForm):
    class Meta:
        model = TicketMilestone
        

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=32)
    

class UserRegisterForm(forms.ModelForm):
    #captcha = ReCaptchaField()
    class Meta:
        model = UserProfile
        exclude = ('avatar', 'wiki_page', 'last_login', 'date_joined', 'rating', 'reputation', 'forum_posts', 'developer')
    def is_valid(self):
        valid = forms.ModelForm.is_valid(self)
        
        if not valid:
            return False
      
        if re.match(r"^[\w\.]+$", self.data['username']) is None:
            valid = False
            self.errors['username'] = 'Username contains invalid characters. Please use only letters, numbers, . and _. '

        if len(self.data['password']) < 6 :
            valid = False
            self.errors['password'] = 'Password too short. Must be at least 6 characters. '
            
        if self.data['password'] != self.data['password2']:
            valid = False
            self.errors['password'] = 'Passwords didn\'t match. '
            
        if email_re.match(self.data['email']) is None:
            valid = False
            self.errors['email'] += 'Please enter a valid email. '
        elif User.objects.filter(email = self.data['email']):
                valid = False
                self.errors['email'] = 'There is another account with this email address. Please enter other email address.'
            
        return valid

    
class UserEditAccountForm(forms.ModelForm):
    #captcha = ReCaptchaField()
    class Meta:
        model = UserProfile
        exclude = ('wiki_page', 'last_login', 'date_joined', 'rating', 'reputation', 'forum_posts', 'username', 'developer')


class WikiRevisionEditForm (forms.ModelForm):
    forum_topic = models.IntegerField()
    class Meta:
        model = WikiRevision
        exclude = ('revision_id', 'date', 'ip', 'wiki_page', 'author')


################## Facebook auth #############################
class FacebookSessionError(Exception):   
    def __init__(self, error_type, message):
        self.message = message
        self.type = error_type
    def get_message(self): 
        return self.message
    def get_type(self):
        return self.type
    def __unicode__(self):
        return u'%s: "%s"' % (self.type, self.message)
        
class FacebookSession(models.Model):

    access_token = models.CharField(max_length=103, unique=True)
    expires = models.IntegerField(null=True)
        
    user = models.ForeignKey(User, null=True)
    uid = models.BigIntegerField(unique=True, null=True)
        
    class Meta:
        unique_together = (('user', 'uid'), ('access_token', 'expires'))
        
    def query(self, object_id, connection_type=None, metadata=False):
        import urllib
        import simplejson
        
        url = 'https://graph.facebook.com/%s' % (object_id)
        if connection_type:
            url += '/%s' % (connection_type)
        
        params = {'access_token': self.access_token}
        if metadata:
            params['metadata'] = 1
         
        url += '?' + urllib.urlencode(params)
        response = simplejson.load(urllib.urlopen(url))
        if 'error' in response:
            error = response['error']
            raise FacebookSessionError(error['type'], error['message'])
        return response


################################# AKISMET #####################################
def on_comment_was_posted(sender, comment, request, *args, **kwargs):
    # spam checking can be enabled/disabled per the comment's target Model
    #if comment.content_type.model_class() != Entry:
    #    return

    from django.contrib.sites.models import Site
    from django.conf import settings

    try:
        from akismet import Akismet
    except:
        return

    # use TypePad's AntiSpam if the key is specified in settings.py
    if hasattr(settings, 'TYPEPAD_ANTISPAM_API_KEY'):
        ak = Akismet(
            key=settings.TYPEPAD_ANTISPAM_API_KEY,
            blog_url='http://%s/' % Site.objects.get(pk=settings.SITE_ID).domain
        )
        ak.baseurl = 'api.antispam.typepad.com/1.1/'
    else:
        ak = Akismet(
            key=settings.AKISMET_API_KEY,
            blog_url='http://%s/' % Site.objects.get(pk=settings.SITE_ID).domain
        )

    if ak.verify_key():
        data = {
            'user_ip': request.META.get('REMOTE_ADDR', '127.0.0.1'),
            'user_agent': request.META.get('HTTP_USER_AGENT', ''),
            'referrer': request.META.get('HTTP_REFERER', ''),
            'comment_type': 'comment',
            'comment_author': comment.user_name.encode('utf-8'),
        }

        if ak.comment_check(comment.comment.encode('utf-8'), data=data, build_data=True):
            comment.flags.create(
                user=comment.content_object.author,
                flag='spam'
            )
            comment.is_public = False
            comment.save()

#comment_was_posted.connect(on_comment_was_posted)
