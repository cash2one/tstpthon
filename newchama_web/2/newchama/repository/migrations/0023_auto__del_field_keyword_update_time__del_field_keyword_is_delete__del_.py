# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Keyword.update_time'
        db.delete_column(u'repository_keyword', 'update_time')

        # Deleting field 'Keyword.is_delete'
        db.delete_column(u'repository_keyword', 'is_delete')

        # Deleting field 'Keyword.count_project'
        db.delete_column(u'repository_keyword', 'count_project')

        # Deleting field 'Keyword.count_preference'
        db.delete_column(u'repository_keyword', 'count_preference')

        # Deleting field 'Keyword.add_time'
        db.delete_column(u'repository_keyword', 'add_time')


    def backwards(self, orm):
        # Adding field 'Keyword.update_time'
        db.add_column(u'repository_keyword', 'update_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True),
                      keep_default=False)

        # Adding field 'Keyword.is_delete'
        db.add_column(u'repository_keyword', 'is_delete',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Keyword.count_project'
        db.add_column(u'repository_keyword', 'count_project',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Keyword.count_preference'
        db.add_column(u'repository_keyword', 'count_preference',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Keyword.add_time'
        db.add_column(u'repository_keyword', 'add_time',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now),
                      keep_default=False)


    models = {
        u'area.city': {
            'Meta': {'object_name': 'City'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Province']"})
        },
        u'area.continent': {
            'Meta': {'object_name': 'Continent'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'area.country': {
            'Meta': {'object_name': 'Country'},
            'continent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Continent']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'area.province': {
            'Meta': {'object_name': 'Province'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'industry.industry': {
            'Meta': {'object_name': 'Industry'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'father': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['industry.Industry']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'repository.accountingfirm': {
            'Meta': {'object_name': 'AccountingFirm'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'short_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'repository.investmentcompany': {
            'Meta': {'object_name': 'InvestmentCompany'},
            'address_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'capital_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.City']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Country']", 'null': 'True', 'blank': 'True'}),
            'found_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_cn': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'intro_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Province']", 'null': 'True', 'blank': 'True'}),
            'short_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'stock_exchange': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.StockExchange']", 'null': 'True', 'blank': 'True'}),
            'stock_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'stock_symbol_no_pre': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'repository.investmenthistory': {
            'Meta': {'object_name': 'InvestmentHistory'},
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.InvestmentCompany']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'happen_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'repository.keyword': {
            'Meta': {'object_name': 'Keyword'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'})
        },
        u'repository.listedcompany': {
            'Meta': {'object_name': 'ListedCompany'},
            'address_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.City']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Country']", 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'found_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['industry.Industry']", 'null': 'True', 'blank': 'True'}),
            'intro_cn': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'intro_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Province']", 'null': 'True', 'blank': 'True'}),
            'short_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'stock_exchange': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.StockExchange']"}),
            'stock_name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'stock_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'stock_symbol_no_pre': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'repository.stockexchange': {
            'Meta': {'object_name': 'StockExchange'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'short_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['repository']