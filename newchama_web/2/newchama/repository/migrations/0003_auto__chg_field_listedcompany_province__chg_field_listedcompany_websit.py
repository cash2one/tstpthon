# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ListedCompany.province'
        db.alter_column(u'repository_listedcompany', 'province_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.Province'], null=True))

        # Changing field 'ListedCompany.website'
        db.alter_column(u'repository_listedcompany', 'website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

        # Changing field 'ListedCompany.fax'
        db.alter_column(u'repository_listedcompany', 'fax', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'ListedCompany.tel'
        db.alter_column(u'repository_listedcompany', 'tel', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'ListedCompany.industry'
        db.alter_column(u'repository_listedcompany', 'industry_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['industry.Industry'], null=True))

        # Changing field 'ListedCompany.address_cn'
        db.alter_column(u'repository_listedcompany', 'address_cn', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'ListedCompany.postcode'
        db.alter_column(u'repository_listedcompany', 'postcode', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'ListedCompany.country'
        db.alter_column(u'repository_listedcompany', 'country_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.Country'], null=True))

        # Changing field 'ListedCompany.stock_exchange'
        db.alter_column(u'repository_listedcompany', 'stock_exchange_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.StockExchange'], null=True))

        # Changing field 'ListedCompany.address_en'
        db.alter_column(u'repository_listedcompany', 'address_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'ListedCompany.stock_symbol'
        db.alter_column(u'repository_listedcompany', 'stock_symbol', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

    def backwards(self, orm):

        # Changing field 'ListedCompany.province'
        db.alter_column(u'repository_listedcompany', 'province_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['area.Province']))

        # Changing field 'ListedCompany.website'
        db.alter_column(u'repository_listedcompany', 'website', self.gf('django.db.models.fields.URLField')(default=None, max_length=200))

        # Changing field 'ListedCompany.fax'
        db.alter_column(u'repository_listedcompany', 'fax', self.gf('django.db.models.fields.CharField')(default=None, max_length=20))

        # Changing field 'ListedCompany.tel'
        db.alter_column(u'repository_listedcompany', 'tel', self.gf('django.db.models.fields.CharField')(default=None, max_length=20))

        # Changing field 'ListedCompany.industry'
        db.alter_column(u'repository_listedcompany', 'industry_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['industry.Industry']))

        # Changing field 'ListedCompany.address_cn'
        db.alter_column(u'repository_listedcompany', 'address_cn', self.gf('django.db.models.fields.CharField')(default=None, max_length=255))

        # Changing field 'ListedCompany.postcode'
        db.alter_column(u'repository_listedcompany', 'postcode', self.gf('django.db.models.fields.CharField')(default=None, max_length=20))

        # Changing field 'ListedCompany.country'
        db.alter_column(u'repository_listedcompany', 'country_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['area.Country']))

        # Changing field 'ListedCompany.stock_exchange'
        db.alter_column(u'repository_listedcompany', 'stock_exchange_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['repository.StockExchange']))

        # Changing field 'ListedCompany.address_en'
        db.alter_column(u'repository_listedcompany', 'address_en', self.gf('django.db.models.fields.CharField')(default=None, max_length=255))

        # Changing field 'ListedCompany.stock_symbol'
        db.alter_column(u'repository_listedcompany', 'stock_symbol', self.gf('django.db.models.fields.CharField')(default=None, max_length=20))

    models = {
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
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'short_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'})
        },
        u'repository.listedcompany': {
            'Meta': {'object_name': 'ListedCompany'},
            'address_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'address_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Country']", 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['industry.Industry']", 'null': 'True', 'blank': 'True'}),
            'intro_cn': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'intro_en': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'investment_experience_cn': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'investment_experience_en': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Province']", 'null': 'True', 'blank': 'True'}),
            'short_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'stock_exchange': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.StockExchange']", 'null': 'True', 'blank': 'True'}),
            'stock_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        u'repository.stockexchange': {
            'Meta': {'object_name': 'StockExchange'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['repository']