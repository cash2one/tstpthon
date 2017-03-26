# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Industry.father'
        db.add_column(u'industry_industry', 'father',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['industry.Industry'], null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Industry.father'
        db.delete_column(u'industry_industry', 'father_id')


    models = {
        u'industry.industry': {
            'Meta': {'object_name': 'Industry'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'father': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': u"orm['industry.Industry']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['industry']