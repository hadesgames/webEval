# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Eval'
        db.create_table('api_eval', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('public_key', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('private_key', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('compat_factor', self.gf('django.db.models.fields.FloatField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('os', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('updated', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('api', ['Eval'])


    def backwards(self, orm):
        
        # Deleting model 'Eval'
        db.delete_table('api_eval')


    models = {
        'api.eval': {
            'Meta': {'object_name': 'Eval'},
            'compat_factor': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'os': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'private_key': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'public_key': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'updated': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['api']
