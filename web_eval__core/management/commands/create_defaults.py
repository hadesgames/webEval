import datetime
import hashlib

from django.core.management.base import BaseCommand, CommandError
from django.core.urlresolvers import reverse

from webEval.web_eval__core.models import *
from webEval.settings import HOST_URL

class Command(BaseCommand):
    help = 'Creates default entries in database, like default contest, default blog entry, etc'

    def handle(self, *args, **options):
        # Make the first user in system admin.
        try:
            user = User.objects.get()
            
            print "Setting admin flag for user '%s' to true" % user.username
            user.is_superuser = True
            
            print "Setting staff flag for user '%s' to true" % user.username
            user.is_staff = True
            
            print "Setting active flag to user '%s' to true" % user.username
            user.is_active = True
            
            user.save()
            
            print "Saving user '%s', continuing...\n" % user.username
        except:
            print "Cannot get first user, please go to %s%s and register it" % (HOST_URL,
                                                                                 reverse("webEval.web_eval__core.auth__controller.register"))
            return
        
        user = UserProfile.objects.get()
        
        try:
            default_contest = Contest.objects.get(code='none')
            print "Default contest found, continuing...\n"
        except:
            default_contest = Contest()
            default_contest__wiki_page = WikiPage()
            default_contest__wiki_first_revision = WikiRevision()
            
            default_contest__wiki_page.url = reverse("webEval.web_eval__core.grader__controller.display_contest",
                                                     kwargs = {'contest_code' : 'default'}).lstrip('/').rstrip('/')
            default_contest__wiki_page.author = user
            print "Creating wiki page for default contest"
            default_contest__wiki_page.save()
            
            default_contest__wiki_first_revision.revision_id = 1
            default_contest__wiki_first_revision.date = datetime.datetime.now()
            default_contest__wiki_first_revision.ip = '127.0.0.1'
            default_contest__wiki_first_revision.wiki_page = default_contest__wiki_page
            default_contest__wiki_first_revision.markup_type = 'C'
            default_contest__wiki_first_revision.security = 'Protected'
            default_contest__wiki_first_revision.author = user
            default_contest__wiki_first_revision.title = 'Default'
            default_contest__wiki_first_revision.content = """
                == %s ==
                This is the contest that just created problems are connected to.
            """ % 'None'
            default_contest__wiki_first_revision.save()
            default_contest__wiki_page.last_revision = default_contest__wiki_first_revision
            default_contest__wiki_page.save()
            
            default_contest.name = 'Default'
            default_contest.code = 'none'
            default_contest.start_time = datetime.datetime.now()
            default_contest.end_time = datetime.datetime(year=2099, month=12, day=31)
            default_contest.wiki_page = default_contest__wiki_page
            default_contest.type = 'O'
            default_contest.with_rating = False
            default_contest.with_open_eval = True
            print "Creating default contest, continuing...\n"
            default_contest.save()
            
            
        try:
            forum_index = ForumBoard.objects.get(id=1)
            print "Forum board found, continuing...\n"
        except:
            print "Creating forum index...\n"
            forum_index = ForumBoard()
            forum_index.name = 'webEval'
            forum_index.description = 'Forum Index'
            forum_index.topics = 0
            forum_index.posts = 0
            forum_index.public = True
            print "Saving forum index...\n"
            forum_index.save()
            
        
        welcome_blog_post = BlogEntry()
        welcome_blog_post.title = 'Successful install'
        welcome_blog_post.content = 'You have successfully installed webEval.'
        welcome_blog_post.author = user
        welcome_blog_post.permalink = hashlib.md5(str(datetime.datetime.now())).hexdigest()
        welcome_blog_post.date = datetime.datetime.now()
        print "Saving greeting blog entry, ..."
        welcome_blog_post.save()
        print "Adding greeting to dashboard,...\n"
        DashboardEntry(blog_entry=welcome_blog_post).save()
        
        print "Done!\n"
        
