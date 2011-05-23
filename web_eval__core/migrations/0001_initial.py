# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'BlogEntry'
        db.create_table('web_eval__core_blogentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.UserProfile'])),
            ('permalink', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('web_eval__core', ['BlogEntry'])

        # Adding M2M table for field tags on 'BlogEntry'
        db.create_table('web_eval__core_blogentry_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('blogentry', models.ForeignKey(orm['web_eval__core.blogentry'], null=False)),
            ('tag', models.ForeignKey(orm['web_eval__core.tag'], null=False))
        ))
        db.create_unique('web_eval__core_blogentry_tags', ['blogentry_id', 'tag_id'])

        # Adding model 'BlogRollEntry'
        db.create_table('web_eval__core_blogrollentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.UserProfile'])),
            ('link', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('web_eval__core', ['BlogRollEntry'])

        # Adding model 'DashboardEntry'
        db.create_table('web_eval__core_dashboardentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('blog_entry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.BlogEntry'])),
        ))
        db.send_create_signal('web_eval__core', ['DashboardEntry'])

        # Adding model 'Tag'
        db.create_table('web_eval__core_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('uses', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('web_eval__core', ['Tag'])

        # Adding model 'ForumBoard'
        db.create_table('web_eval__core_forumboard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_board', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.ForumBoard'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('topics', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('posts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('last_post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.ForumPost'], null=True, blank=True)),
            ('public', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('web_eval__core', ['ForumBoard'])

        # Adding model 'ForumTopic'
        db.create_table('web_eval__core_forumtopic', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('board', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.ForumBoard'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.UserProfile'])),
            ('first_post', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='first_post', null=True, to=orm['web_eval__core.ForumPost'])),
            ('last_post', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='last_post', null=True, to=orm['web_eval__core.ForumPost'])),
            ('views', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('posts', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('web_eval__core', ['ForumTopic'])

        # Adding model 'ForumPost'
        db.create_table('web_eval__core_forumpost', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.ForumTopic'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.UserProfile'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('web_eval__core', ['ForumPost'])

        # Adding model 'CalendarEntry'
        db.create_table('web_eval__core_calendarentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('forum_topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.ForumTopic'], null=True)),
        ))
        db.send_create_signal('web_eval__core', ['CalendarEntry'])

        # Adding model 'PrivateMessage'
        db.create_table('web_eval__core_privatemessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('user_from', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_from', to=orm['web_eval__core.UserProfile'])),
            ('user_to', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_to', to=orm['web_eval__core.UserProfile'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('web_eval__core', ['PrivateMessage'])

        # Adding model 'Author'
        db.create_table('web_eval__core_author', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
        ))
        db.send_create_signal('web_eval__core', ['Author'])

        # Adding model 'Contest'
        db.create_table('web_eval__core_contest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('wiki_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.WikiPage'])),
            ('type', self.gf('django.db.models.fields.CharField')(default='C', max_length=1)),
            ('with_rating', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('with_open_eval', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('web_eval__core', ['Contest'])

        # Adding M2M table for field problems on 'Contest'
        db.create_table('web_eval__core_contest_problems', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contest', models.ForeignKey(orm['web_eval__core.contest'], null=False)),
            ('problem', models.ForeignKey(orm['web_eval__core.problem'], null=False))
        ))
        db.create_unique('web_eval__core_contest_problems', ['contest_id', 'problem_id'])

        # Adding M2M table for field registered_users on 'Contest'
        db.create_table('web_eval__core_contest_registered_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contest', models.ForeignKey(orm['web_eval__core.contest'], null=False)),
            ('userprofile', models.ForeignKey(orm['web_eval__core.userprofile'], null=False))
        ))
        db.create_unique('web_eval__core_contest_registered_users', ['contest_id', 'userprofile_id'])

        # Adding model 'Problem'
        db.create_table('web_eval__core_problem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=16)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.UserProfile'])),
            ('resource', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.Contest'])),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.Author'])),
            ('time_limit', self.gf('django.db.models.fields.IntegerField')()),
            ('memory_limit', self.gf('django.db.models.fields.IntegerField')()),
            ('source_limit', self.gf('django.db.models.fields.IntegerField')()),
            ('forum_topic', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.ForumTopic'], null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='Normal', max_length=16)),
            ('wiki_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.WikiPage'])),
        ))
        db.send_create_signal('web_eval__core', ['Problem'])

        # Adding M2M table for field tags on 'Problem'
        db.create_table('web_eval__core_problem_tags', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('problem', models.ForeignKey(orm['web_eval__core.problem'], null=False)),
            ('tag', models.ForeignKey(orm['web_eval__core.tag'], null=False))
        ))
        db.create_unique('web_eval__core_problem_tags', ['problem_id', 'tag_id'])

        # Adding model 'Job'
        db.create_table('web_eval__core_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('problem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.Problem'])),
            ('contest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.Contest'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.UserProfile'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('percent_completed', self.gf('django.db.models.fields.IntegerField')()),
            ('processing', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('language', self.gf('django.db.models.fields.CharField')(default='cpp', max_length=4)),
            ('source_size', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('private', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('web_eval__core', ['Job'])

        # Adding model 'Test'
        db.create_table('web_eval__core_test', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.Job'])),
            ('no', self.gf('django.db.models.fields.IntegerField')()),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
            ('memory', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('time', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('web_eval__core', ['Test'])

        # Adding model 'GraderTest'
        db.create_table('web_eval__core_gradertest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('no', self.gf('django.db.models.fields.IntegerField')()),
            ('problem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.Problem'])),
            ('time', self.gf('django.db.models.fields.IntegerField')(default=1000)),
            ('memory', self.gf('django.db.models.fields.IntegerField')(default=16384)),
            ('group', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('input_size', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('output_size', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('feedback', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('web_eval__core', ['GraderTest'])

        # Adding model 'RatingCache'
        db.create_table('web_eval__core_ratingcache', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rating', self.gf('django.db.models.fields.IntegerField')()),
            ('contest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.Contest'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.UserProfile'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('web_eval__core', ['RatingCache'])

        # Adding model 'ScoreCache'
        db.create_table('web_eval__core_scorecache', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.Contest'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.UserProfile'])),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('web_eval__core', ['ScoreCache'])

        # Adding model 'ScoreProblemCache'
        db.create_table('web_eval__core_scoreproblemcache', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('problem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.Problem'])),
            ('cache', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.ScoreCache'])),
            ('score', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('web_eval__core', ['ScoreProblemCache'])

        # Adding model 'UserProfile'
        db.create_table('web_eval__core_userprofile', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('avatar', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('wiki_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.WikiPage'], null=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('rating', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('facebook_uid', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('twitter_user', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('reputation', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('forum_posts', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('developer', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('web_eval__core', ['UserProfile'])

        # Adding model 'UserValidationKey'
        db.create_table('web_eval__core_uservalidationkey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('username', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.UserProfile'])),
            ('expire_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('web_eval__core', ['UserValidationKey'])

        # Adding model 'WikiPage'
        db.create_table('web_eval__core_wikipage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.UserProfile'])),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128, blank=True)),
            ('last_revision', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['web_eval__core.WikiRevision'], null=True, blank=True)),
        ))
        db.send_create_signal('web_eval__core', ['WikiPage'])

        # Adding model 'WikiRevision'
        db.create_table('web_eval__core_wikirevision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('revision_id', self.gf('django.db.models.fields.IntegerField')()),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('wiki_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.WikiPage'])),
            ('markup_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('security', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.UserProfile'])),
        ))
        db.send_create_signal('web_eval__core', ['WikiRevision'])

        # Adding model 'WikiAttachment'
        db.create_table('web_eval__core_wikiattachment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('wiki_page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.WikiPage'])),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('size', self.gf('django.db.models.fields.IntegerField')()),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('hash', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('security', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('web_eval__core', ['WikiAttachment'])

        # Adding model 'TicketMilestone'
        db.create_table('web_eval__core_ticketmilestone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('version', self.gf('django.db.models.fields.FloatField')(unique=True)),
            ('due', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('web_eval__core', ['TicketMilestone'])

        # Adding model 'Ticket'
        db.create_table('web_eval__core_ticket', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_posted', self.gf('django.db.models.fields.DateTimeField')()),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('severity', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('milestone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.TicketMilestone'], null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.UserProfile'])),
            ('assignee', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name='assignee', null=True, blank=True, to=orm['web_eval__core.UserProfile'])),
        ))
        db.send_create_signal('web_eval__core', ['Ticket'])

        # Adding model 'TicketComment'
        db.create_table('web_eval__core_ticketcomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date_posted', self.gf('django.db.models.fields.DateTimeField')()),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.UserProfile'])),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('ticket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.Ticket'])),
            ('autogenerated', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('web_eval__core', ['TicketComment'])

        # Adding model 'FacebookSession'
        db.create_table('web_eval__core_facebooksession', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('access_token', self.gf('django.db.models.fields.CharField')(unique=True, max_length=103)),
            ('expires', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('uid', self.gf('django.db.models.fields.BigIntegerField')(unique=True, null=True)),
        ))
        db.send_create_signal('web_eval__core', ['FacebookSession'])

        # Adding unique constraint on 'FacebookSession', fields ['user', 'uid']
        db.create_unique('web_eval__core_facebooksession', ['user_id', 'uid'])

        # Adding unique constraint on 'FacebookSession', fields ['access_token', 'expires']
        db.create_unique('web_eval__core_facebooksession', ['access_token', 'expires'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'FacebookSession', fields ['access_token', 'expires']
        db.delete_unique('web_eval__core_facebooksession', ['access_token', 'expires'])

        # Removing unique constraint on 'FacebookSession', fields ['user', 'uid']
        db.delete_unique('web_eval__core_facebooksession', ['user_id', 'uid'])

        # Deleting model 'BlogEntry'
        db.delete_table('web_eval__core_blogentry')

        # Removing M2M table for field tags on 'BlogEntry'
        db.delete_table('web_eval__core_blogentry_tags')

        # Deleting model 'BlogRollEntry'
        db.delete_table('web_eval__core_blogrollentry')

        # Deleting model 'DashboardEntry'
        db.delete_table('web_eval__core_dashboardentry')

        # Deleting model 'Tag'
        db.delete_table('web_eval__core_tag')

        # Deleting model 'ForumBoard'
        db.delete_table('web_eval__core_forumboard')

        # Deleting model 'ForumTopic'
        db.delete_table('web_eval__core_forumtopic')

        # Deleting model 'ForumPost'
        db.delete_table('web_eval__core_forumpost')

        # Deleting model 'CalendarEntry'
        db.delete_table('web_eval__core_calendarentry')

        # Deleting model 'PrivateMessage'
        db.delete_table('web_eval__core_privatemessage')

        # Deleting model 'Author'
        db.delete_table('web_eval__core_author')

        # Deleting model 'Contest'
        db.delete_table('web_eval__core_contest')

        # Removing M2M table for field problems on 'Contest'
        db.delete_table('web_eval__core_contest_problems')

        # Removing M2M table for field registered_users on 'Contest'
        db.delete_table('web_eval__core_contest_registered_users')

        # Deleting model 'Problem'
        db.delete_table('web_eval__core_problem')

        # Removing M2M table for field tags on 'Problem'
        db.delete_table('web_eval__core_problem_tags')

        # Deleting model 'Job'
        db.delete_table('web_eval__core_job')

        # Deleting model 'Test'
        db.delete_table('web_eval__core_test')

        # Deleting model 'GraderTest'
        db.delete_table('web_eval__core_gradertest')

        # Deleting model 'RatingCache'
        db.delete_table('web_eval__core_ratingcache')

        # Deleting model 'ScoreCache'
        db.delete_table('web_eval__core_scorecache')

        # Deleting model 'ScoreProblemCache'
        db.delete_table('web_eval__core_scoreproblemcache')

        # Deleting model 'UserProfile'
        db.delete_table('web_eval__core_userprofile')

        # Deleting model 'UserValidationKey'
        db.delete_table('web_eval__core_uservalidationkey')

        # Deleting model 'WikiPage'
        db.delete_table('web_eval__core_wikipage')

        # Deleting model 'WikiRevision'
        db.delete_table('web_eval__core_wikirevision')

        # Deleting model 'WikiAttachment'
        db.delete_table('web_eval__core_wikiattachment')

        # Deleting model 'TicketMilestone'
        db.delete_table('web_eval__core_ticketmilestone')

        # Deleting model 'Ticket'
        db.delete_table('web_eval__core_ticket')

        # Deleting model 'TicketComment'
        db.delete_table('web_eval__core_ticketcomment')

        # Deleting model 'FacebookSession'
        db.delete_table('web_eval__core_facebooksession')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'web_eval__core.author': {
            'Meta': {'object_name': 'Author'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'web_eval__core.blogentry': {
            'Meta': {'object_name': 'BlogEntry'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.UserProfile']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permalink': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['web_eval__core.Tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'web_eval__core.blogrollentry': {
            'Meta': {'object_name': 'BlogRollEntry'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.UserProfile']"})
        },
        'web_eval__core.calendarentry': {
            'Meta': {'object_name': 'CalendarEntry'},
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'forum_topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.ForumTopic']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'web_eval__core.contest': {
            'Meta': {'object_name': 'Contest'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'problems': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['web_eval__core.Problem']", 'symmetrical': 'False'}),
            'registered_users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['web_eval__core.UserProfile']", 'symmetrical': 'False'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'C'", 'max_length': '1'}),
            'wiki_page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.WikiPage']"}),
            'with_open_eval': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'with_rating': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'web_eval__core.dashboardentry': {
            'Meta': {'object_name': 'DashboardEntry'},
            'blog_entry': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.BlogEntry']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'web_eval__core.facebooksession': {
            'Meta': {'unique_together': "(('user', 'uid'), ('access_token', 'expires'))", 'object_name': 'FacebookSession'},
            'access_token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '103'}),
            'expires': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uid': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'web_eval__core.forumboard': {
            'Meta': {'object_name': 'ForumBoard'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.ForumPost']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'parent_board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.ForumBoard']", 'null': 'True', 'blank': 'True'}),
            'posts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'topics': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'web_eval__core.forumpost': {
            'Meta': {'object_name': 'ForumPost'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.UserProfile']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.ForumTopic']"})
        },
        'web_eval__core.forumtopic': {
            'Meta': {'object_name': 'ForumTopic'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.UserProfile']"}),
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.ForumBoard']"}),
            'first_post': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'first_post'", 'null': 'True', 'to': "orm['web_eval__core.ForumPost']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_post': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'last_post'", 'null': 'True', 'to': "orm['web_eval__core.ForumPost']"}),
            'posts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'views': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'web_eval__core.gradertest': {
            'Meta': {'object_name': 'GraderTest'},
            'feedback': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'group': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'input_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'memory': ('django.db.models.fields.IntegerField', [], {'default': '16384'}),
            'no': ('django.db.models.fields.IntegerField', [], {}),
            'output_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.Problem']"}),
            'time': ('django.db.models.fields.IntegerField', [], {'default': '1000'})
        },
        'web_eval__core.job': {
            'Meta': {'object_name': 'Job'},
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.Contest']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'cpp'", 'max_length': '4'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'percent_completed': ('django.db.models.fields.IntegerField', [], {}),
            'private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.Problem']"}),
            'processing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'score': ('django.db.models.fields.IntegerField', [], {}),
            'source_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.UserProfile']"})
        },
        'web_eval__core.privatemessage': {
            'Meta': {'object_name': 'PrivateMessage'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_from'", 'to': "orm['web_eval__core.UserProfile']"}),
            'user_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_to'", 'to': "orm['web_eval__core.UserProfile']"})
        },
        'web_eval__core.problem': {
            'Meta': {'object_name': 'Problem'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.Author']"}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '16'}),
            'forum_topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.ForumTopic']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'memory_limit': ('django.db.models.fields.IntegerField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.UserProfile']"}),
            'resource': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.Contest']"}),
            'source_limit': ('django.db.models.fields.IntegerField', [], {}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['web_eval__core.Tag']", 'symmetrical': 'False'}),
            'time_limit': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'Normal'", 'max_length': '16'}),
            'wiki_page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.WikiPage']"})
        },
        'web_eval__core.ratingcache': {
            'Meta': {'object_name': 'RatingCache'},
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.Contest']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.UserProfile']"})
        },
        'web_eval__core.scorecache': {
            'Meta': {'object_name': 'ScoreCache'},
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.Contest']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.UserProfile']"})
        },
        'web_eval__core.scoreproblemcache': {
            'Meta': {'object_name': 'ScoreProblemCache'},
            'cache': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.ScoreCache']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.Problem']"}),
            'score': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'web_eval__core.tag': {
            'Meta': {'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'uses': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'web_eval__core.test': {
            'Meta': {'object_name': 'Test'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.Job']"}),
            'memory': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'no': ('django.db.models.fields.IntegerField', [], {}),
            'score': ('django.db.models.fields.IntegerField', [], {}),
            'time': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'web_eval__core.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'assignee': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'assignee'", 'null': 'True', 'blank': 'True', 'to': "orm['web_eval__core.UserProfile']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.UserProfile']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_posted': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'milestone': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.TicketMilestone']", 'null': 'True', 'blank': 'True'}),
            'severity': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'web_eval__core.ticketcomment': {
            'Meta': {'object_name': 'TicketComment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.UserProfile']"}),
            'autogenerated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_posted': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ticket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.Ticket']"})
        },
        'web_eval__core.ticketmilestone': {
            'Meta': {'object_name': 'TicketMilestone'},
            'due': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'version': ('django.db.models.fields.FloatField', [], {'unique': 'True'})
        },
        'web_eval__core.userprofile': {
            'Meta': {'object_name': 'UserProfile', '_ormbases': ['auth.User']},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'developer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facebook_uid': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'forum_posts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'reputation': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'twitter_user': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'}),
            'wiki_page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.WikiPage']", 'null': 'True'})
        },
        'web_eval__core.uservalidationkey': {
            'Meta': {'object_name': 'UserValidationKey'},
            'expire_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'username': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.UserProfile']"})
        },
        'web_eval__core.wikiattachment': {
            'Meta': {'object_name': 'WikiAttachment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'hash': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'security': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'size': ('django.db.models.fields.IntegerField', [], {}),
            'wiki_page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.WikiPage']"})
        },
        'web_eval__core.wikipage': {
            'Meta': {'object_name': 'WikiPage'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.UserProfile']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_revision': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['web_eval__core.WikiRevision']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128', 'blank': 'True'})
        },
        'web_eval__core.wikirevision': {
            'Meta': {'object_name': 'WikiRevision'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.UserProfile']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'markup_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'revision_id': ('django.db.models.fields.IntegerField', [], {}),
            'security': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'wiki_page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.WikiPage']"})
        }
    }

    complete_apps = ['web_eval__core']
