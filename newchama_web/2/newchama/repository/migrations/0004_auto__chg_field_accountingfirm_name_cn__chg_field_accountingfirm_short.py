# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'AccountingFirm.name_cn'
        db.alter_column(u'repository_accountingfirm', 'name_cn', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'AccountingFirm.short_name_cn'
        db.alter_column(u'repository_accountingfirm', 'short_name_cn', self.gf('django.db.models.fields.CharField')(default='', max_length=20))

        # Changing field 'AccountingFirm.name_en'
        db.alter_column(u'repository_accountingfirm', 'name_en', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'AccountingFirm.short_name_en'
        db.alter_column(u'repository_accountingfirm', 'short_name_en', self.gf('django.db.models.fields.CharField')(default='', max_length=20))

        # Changing field 'ListedCompany.province'
        db.alter_column(u'repository_listedcompany', 'province_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.Province']))

        # Changing field 'ListedCompany.website'
        db.alter_column(u'repository_listedcompany', 'website', self.gf('django.db.models.fields.URLField')(default='', max_length=200))

        # Changing field 'ListedCompany.fax'
        db.alter_column(u'repository_listedcompany', 'fax', self.gf('django.db.models.fields.CharField')(default='', max_length=20))

        # Changing field 'ListedCompany.tel'
        db.alter_column(u'repository_listedcompany', 'tel', self.gf('django.db.models.fields.CharField')(default='', max_length=20))

        # Changing field 'ListedCompany.name_en'
        db.alter_column(u'repository_listedcompany', 'name_en', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'ListedCompany.name_cn'
        db.alter_column(u'repository_listedcompany', 'name_cn', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'ListedCompany.industry'
        db.alter_column(u'repository_listedcompany', 'industry_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['industry.Industry']))

        # Changing field 'ListedCompany.investment_experience_en'
        db.alter_column(u'repository_listedcompany', 'investment_experience_en', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'ListedCompany.address_cn'
        db.alter_column(u'repository_listedcompany', 'address_cn', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'ListedCompany.intro_en'
        db.alter_column(u'repository_listedcompany', 'intro_en', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'ListedCompany.postcode'
        db.alter_column(u'repository_listedcompany', 'postcode', self.gf('django.db.models.fields.CharField')(default='', max_length=20))

        # Changing field 'ListedCompany.short_name_en'
        db.alter_column(u'repository_listedcompany', 'short_name_en', self.gf('django.db.models.fields.CharField')(default='', max_length=20))

        # Changing field 'ListedCompany.country'
        db.alter_column(u'repository_listedcompany', 'country_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.Country']))

        # Changing field 'ListedCompany.intro_cn'
        db.alter_column(u'repository_listedcompany', 'intro_cn', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'ListedCompany.stock_exchange'
        db.alter_column(u'repository_listedcompany', 'stock_exchange_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.StockExchange']))

        # Changing field 'ListedCompany.address_en'
        db.alter_column(u'repository_listedcompany', 'address_en', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'ListedCompany.stock_symbol'
        db.alter_column(u'repository_listedcompany', 'stock_symbol', self.gf('django.db.models.fields.CharField')(default='', max_length=20))

        # Changing field 'ListedCompany.investment_experience_cn'
        db.alter_column(u'repository_listedcompany', 'investment_experience_cn', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'ListedCompany.short_name_cn'
        db.alter_column(u'repository_listedcompany', 'short_name_cn', self.gf('django.db.models.fields.CharField')(default='', max_length=20))

    def backwards(self, orm):

        # Changing field 'AccountingFirm.name_cn'
        db.alter_column(u'repository_accountingfirm', 'name_cn', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'AccountingFirm.short_name_cn'
        db.alter_column(u'repository_accountingfirm', 'short_name_cn', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'AccountingFirm.name_en'
        db.alter_column(u'repository_accountingfirm', 'name_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'AccountingFirm.short_name_en'
        db.alter_column(u'repository_accountingfirm', 'short_name_en', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'ListedCompany.province'
        db.alter_column(u'repository_listedcompany', 'province_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.Province'], null=True))

        # Changing field 'ListedCompany.website'
        db.alter_column(u'repository_listedcompany', 'website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

        # Changing field 'ListedCompany.fax'
        db.alter_column(u'repository_listedcompany', 'fax', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'ListedCompany.tel'
        db.alter_column(u'repository_listedcompany', 'tel', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'ListedCompany.name_en'
        db.alter_column(u'repository_listedcompany', 'name_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'ListedCompany.name_cn'
        db.alter_column(u'repository_listedcompany', 'name_cn', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'ListedCompany.industry'
        db.alter_column(u'repository_listedcompany', 'industry_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['industry.Industry'], null=True))

        # Changing field 'ListedCompany.investment_experience_en'
        db.alter_column(u'repository_listedcompany', 'investment_experience_en', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'ListedCompany.address_cn'
        db.alter_column(u'repository_listedcompany', 'address_cn', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'ListedCompany.intro_en'
        db.alter_column(u'repository_listedcompany', 'intro_en', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'ListedCompany.postcode'
        db.alter_column(u'repository_listedcompany', 'postcode', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'ListedCompany.short_name_en'
        db.alter_column(u'repository_listedcompany', 'short_name_en', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'ListedCompany.country'
        db.alter_column(u'repository_listedcompany', 'country_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.Country'], null=True))

        # Changing field 'ListedCompany.intro_cn'
        db.alter_column(u'repository_listedcompany', 'intro_cn', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'ListedCompany.stock_exchange'
        db.alter_column(u'repository_listedcompany', 'stock_exchange_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.StockExchange'], null=True))

        # Changing field 'ListedCompany.address_en'
        db.alter_column(u'repository_listedcompany', 'address_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'ListedCompany.stock_symbol'
        db.alter_column(u'repository_listedcompany', 'stock_symbol', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'ListedCompany.investment_experience_cn'
        db.alter_column(u'repository_listedcompany', 'investment_experience_cn', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'ListedCompany.short_name_cn'
        db.alter_column(u'repository_listedcompany', 'short_name_cn', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

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
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'short_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'repository.listedcompany': {
            'Meta': {'object_name': 'ListedCompany'},
            'address_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'address_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': u"orm['area.Country']", 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': u"orm['industry.Industry']", 'blank': 'True'}),
            'intro_cn': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'intro_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'investment_experience_cn': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'investment_experience_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': u"orm['area.Province']", 'blank': 'True'}),
            'short_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'stock_exchange': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'to': u"orm['repository.StockExchange']", 'blank': 'True'}),
            'stock_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'repository.stockexchange': {
            'Meta': {'object_name': 'StockExchange'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['repository']