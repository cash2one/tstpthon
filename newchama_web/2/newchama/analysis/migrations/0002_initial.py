# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AnalysisUserTotal'
        db.create_table(u'analysis_analysisusertotal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('user_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('project_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('demand_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('listed_user_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('unlisted_user_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('vc_user_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('fa_user_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal(u'analysis', ['AnalysisUserTotal'])

        # Adding model 'AnalysisUser'
        db.create_table(u'analysis_analysisuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('logined_user_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('add_user_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('created_project_user_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('created_demand_user_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('unpublish_user_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('sendmail_user_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal(u'analysis', ['AnalysisUser'])

        # Adding model 'AnalysisProject'
        db.create_table(u'analysis_analysisproject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('all_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('valid_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('created_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('audit_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('offline_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('pendding_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('draft_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('user_add_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('bd_add_num', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
        ))
        db.send_create_signal(u'analysis', ['AnalysisProject'])


    def backwards(self, orm):
        # Deleting model 'AnalysisUserTotal'
        db.delete_table(u'analysis_analysisusertotal')

        # Deleting model 'AnalysisUser'
        db.delete_table(u'analysis_analysisuser')

        # Deleting model 'AnalysisProject'
        db.delete_table(u'analysis_analysisproject')


    models = {
        u'analysis.analysisproject': {
            'Meta': {'object_name': 'AnalysisProject'},
            'all_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'audit_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'bd_add_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'created_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'draft_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offline_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'pendding_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_add_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'valid_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        u'analysis.analysisuser': {
            'Meta': {'object_name': 'AnalysisUser'},
            'add_user_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'created_demand_user_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'created_project_user_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logined_user_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'sendmail_user_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'unpublish_user_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        u'analysis.analysisusertotal': {
            'Meta': {'object_name': 'AnalysisUserTotal'},
            'demand_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'fa_user_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'listed_user_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'project_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'unlisted_user_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'user_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'vc_user_num': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['analysis']