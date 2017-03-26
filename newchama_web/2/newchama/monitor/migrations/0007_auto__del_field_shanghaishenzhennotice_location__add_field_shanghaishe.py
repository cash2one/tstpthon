# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ShanghaiShenzhenNotice.location'
        # db.delete_column(u'monitor_shanghaishenzhennotice', 'location')

        # Adding field 'ShanghaiShenzhenNotice.market_type'
        # db.add_column(u'monitor_shanghaishenzhennotice', 'market_type',
        #               self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monitor.StockMarket'], null=True, blank=True),
        #               keep_default=False)
        #
        #
        # # Renaming column for 'ShanghaiShenzhenNotice.notice_type' to match new field type.
        # db.rename_column(u'monitor_shanghaishenzhennotice', 'notice_type', 'notice_type_id')
        # # Changing field 'ShanghaiShenzhenNotice.notice_type'
        # db.alter_column(u'monitor_shanghaishenzhennotice', 'notice_type_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monitor.ShanghaiShenzhenNoticeType'], null=True))
        # # Adding index on 'ShanghaiShenzhenNotice', fields ['notice_type']
        db.create_index(u'monitor_shanghaishenzhennotice', ['notice_type_id'])


    def backwards(self, orm):
        # Removing index on 'ShanghaiShenzhenNotice', fields ['notice_type']
        # db.delete_index(u'monitor_shanghaishenzhennotice', ['notice_type_id'])
        #
        # # Adding field 'ShanghaiShenzhenNotice.location'
        # # db.add_column(u'monitor_shanghaishenzhennotice', 'location',
        # #               self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
        # #               keep_default=False)
        #
        # # Deleting field 'ShanghaiShenzhenNotice.market_type'
        # db.delete_column(u'monitor_shanghaishenzhennotice', 'market_type_id')
        #
        #
        # # Renaming column for 'ShanghaiShenzhenNotice.notice_type' to match new field type.
        # db.rename_column(u'monitor_shanghaishenzhennotice', 'notice_type_id', 'notice_type')
        # # Changing field 'ShanghaiShenzhenNotice.notice_type'
        db.alter_column(u'monitor_shanghaishenzhennotice', 'notice_type', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

    models = {
        u'monitor.hknotice': {
            'Meta': {'object_name': 'HkNotice'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stock_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'types': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['monitor.HkNoticeType']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'monitor.hknoticetype': {
            'Meta': {'object_name': 'HkNoticeType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'notice_type_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'parent_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        u'monitor.investevent': {
            'Meta': {'object_name': 'InvestEvent'},
            'amount': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
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
        },
        u'monitor.shanghaishenzhennotice': {
            'Meta': {'object_name': 'ShanghaiShenzhenNotice'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitor.StockMarket']", 'null': 'True', 'blank': 'True'}),
            'notice_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitor.ShanghaiShenzhenNoticeType']", 'null': 'True', 'blank': 'True'}),
            'pdf_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        u'monitor.shanghaishenzhennoticetype': {
            'Meta': {'object_name': 'ShanghaiShenzhenNoticeType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'type_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        },
        u'monitor.stockmarket': {
            'Meta': {'object_name': 'StockMarket'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['monitor']