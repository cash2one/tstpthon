# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Role'
        db.create_table(u'adminuser_role', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('permission', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'adminuser', ['Role'])

        # Adding model 'AdminUser'
        db.create_table(u'adminuser_adminuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=255)),
            ('realname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('mobile', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('isactive', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'adminuser', ['AdminUser'])

        # Adding M2M table for field role on 'AdminUser'
        m2m_table_name = db.shorten_name(u'adminuser_adminuser_role')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('adminuser', models.ForeignKey(orm[u'adminuser.adminuser'], null=False)),
            ('role', models.ForeignKey(orm[u'adminuser.role'], null=False))
        ))
        db.create_unique(m2m_table_name, ['adminuser_id', 'role_id'])


    def backwards(self, orm):
        # Deleting model 'Role'
        db.delete_table(u'adminuser_role')

        # Deleting model 'AdminUser'
        db.delete_table(u'adminuser_adminuser')

        # Removing M2M table for field role on 'AdminUser'
        db.delete_table(db.shorten_name(u'adminuser_adminuser_role'))


    models = {
        u'adminuser.adminuser': {
            'Meta': {'object_name': 'AdminUser'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isactive': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'realname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'role': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['adminuser.Role']", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'adminuser.role': {
            'Meta': {'object_name': 'Role'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'permission': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['adminuser']