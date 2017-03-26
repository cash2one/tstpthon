# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'InvestEvent.financial_advisor'
        db.add_column(u'monitor_investevent', 'financial_advisor',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True),
                      keep_default=False)

        # Adding field 'DailyDeal.financial_advisor'
        db.add_column(u'monitor_dailydeal', 'financial_advisor',
                      self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'InvestEvent.financial_advisor'
        db.delete_column(u'monitor_investevent', 'financial_advisor')

        # Deleting field 'DailyDeal.financial_advisor'
        db.delete_column(u'monitor_dailydeal', 'financial_advisor')


    models = {
        u'industry.industry': {
            'Meta': {'object_name': 'Industry'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'father': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['industry.Industry']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'monitor.dailydeal': {
            'Meta': {'object_name': 'DailyDeal'},
            'company_full_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'company_short_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'cv1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'daily_deal_cv1'", 'null': 'True', 'to': u"orm['industry.Industry']"}),
            'cv2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'daily_deal_cv2'", 'null': 'True', 'to': u"orm['industry.Industry']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'deal_amount': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deal_content': ('django.db.models.fields.TextField', [], {}),
            'deal_currency': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'deal_ratio': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'deal_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'financial_advisor': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'stock_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'target_company': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        },
        u'monitor.hknotice': {
            'Meta': {'object_name': 'HkNotice'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
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
            'city': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'cv1': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'cv1'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['industry.Industry']"}),
            'cv2': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'cv2'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['industry.Industry']"}),
            'cv3': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'cv3'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['industry.Industry']"}),
            'data_source': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'event_scene': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'financial_advisor': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('django.db.models.fields.TextField', [], {}),
            'invest_phase': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'investee_abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'investee_fullname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'investors': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'scale': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
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