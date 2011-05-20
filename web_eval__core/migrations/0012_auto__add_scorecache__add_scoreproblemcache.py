# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'ScoreCache'
        db.create_table('web_eval__core_scorecache', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.Contest'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.UserProfile'])),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('web_eval__core', ['ScoreCache'])

        # Adding model 'ScoreProblemCache'
        db.create_table('web_eval__core_scoreproblemcache', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('problem', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.Problem'])),
            ('cache', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web_eval__core.ScoreCache'])),
            ('score', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('web_eval__core', ['ScoreProblemCache'])


    def backwards(self, orm):
        
        # Deleting model 'ScoreCache'
        db.delete_table('web_eval__core_scorecache')

        # Deleting model 'ScoreProblemCache'
        db.delete_table('web_eval__core_scoreproblemcache')


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
            'score': ('django.db.models.fields.IntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.UserProfile']"})
        },
        'web_eval__core.scoreproblemcache': {
            'Meta': {'object_name': 'ScoreProblemCache'},
            'cache': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.ScoreCache']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.Problem']"}),
            'score': ('django.db.models.fields.IntegerField', [], {})
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
            'assignee': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "'assignee'", 'null': 'True', 'to': "orm['web_eval__core.UserProfile']"}),
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
