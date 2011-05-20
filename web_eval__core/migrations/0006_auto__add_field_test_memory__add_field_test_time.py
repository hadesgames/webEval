# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Test.memory'
        db.add_column('web_eval__core_test', 'memory', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Test.time'
        db.add_column('web_eval__core_test', 'time', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Test.memory'
        db.delete_column('web_eval__core_test', 'memory')

        # Deleting field 'Test.time'
        db.delete_column('web_eval__core_test', 'time')


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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'web_eval__core.contest': {
            'Meta': {'object_name': 'Contest'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'problems': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['web_eval__core.Problem']", 'symmetrical': 'False'}),
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
        'web_eval__core.forumboard': {
            'Meta': {'object_name': 'ForumBoard'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.ForumPost']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'parent_board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.ForumBoard']", 'null': 'True', 'blank': 'True'}),
            'posts': ('django.db.models.fields.IntegerField', [], {}),
            'public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'topics': ('django.db.models.fields.IntegerField', [], {})
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
            'first_post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'first_post'", 'to': "orm['web_eval__core.ForumPost']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_post': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'last_post'", 'to': "orm['web_eval__core.ForumPost']"}),
            'posts': ('django.db.models.fields.IntegerField', [], {}),
            'views': ('django.db.models.fields.IntegerField', [], {})
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
            'proccessing': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'source_size': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.UserProfile']"})
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
            'time_limit': ('django.db.models.fields.IntegerField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'wiki_page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.WikiPage']"})
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
        'web_eval__core.userprofile': {
            'Meta': {'object_name': 'UserProfile', '_ormbases': ['auth.User']},
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'profile_description': ('django.db.models.fields.TextField', [], {}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'web_eval__core.uservalidationkey': {
            'Meta': {'object_name': 'UserValidationKey'},
            'expire_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'username': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web_eval__core.UserProfile']"})
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
