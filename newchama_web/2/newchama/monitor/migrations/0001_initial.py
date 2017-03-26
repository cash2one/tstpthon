# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InvestEvent'
        db.create_table(u'monitor_investevent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('investee_abbreviation', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('website_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('industry', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('sub_industry', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('sub_location', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('investee_fullname', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('introduction', self.gf('django.db.models.fields.TextField')()),
            ('invest_phase', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('scale', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('investors', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('data_source', self.gf('django.db.models.fields.CharField')(max_length=40, null=True)),
            ('source_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True)),
        ))
        db.send_create_signal(u'monitor', ['InvestEvent'])


    def backwards(self, orm):
        # Deleting model 'InvestEvent'
        db.delete_table(u'monitor_investevent')


    models = {
        u'monitor.investevent': {
            'Meta': {'object_name': 'InvestEvent'},
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'data_source': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'introduction': ('django.db.models.fields.TextField', [], {}),
            'invest_phase': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'investee_abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'investee_fullname': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'investors': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'scale': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'sub_industry': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'sub_location': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'website_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['monitor']