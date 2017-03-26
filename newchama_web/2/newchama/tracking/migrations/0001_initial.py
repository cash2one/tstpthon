# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TrackingItem'
        db.create_table('tracking_tracking', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['adminuser.AdminUser'])),
            ('tracking_type', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('tracking_id', self.gf('django.db.models.fields.IntegerField')(default=0, null=True)),
            ('tracking_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True)),
            ('add_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'tracking', ['TrackingItem'])


    def backwards(self, orm):
        # Deleting model 'TrackingItem'
        db.delete_table('tracking_tracking')


    models = {
        u'adminuser.adminuser': {
            'Meta': {'object_name': 'AdminUser'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isactive': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'realname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'role': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['adminuser.Role']", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'adminuser.role': {
            'Meta': {'object_name': 'Role'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'permission': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'tracking.trackingitem': {
            'Meta': {'object_name': 'TrackingItem', 'db_table': "'tracking_tracking'"},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tracking_id': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'tracking_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'tracking_type': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['adminuser.AdminUser']"})
        }
    }

    complete_apps = ['tracking']