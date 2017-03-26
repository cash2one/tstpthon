# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AccountingFirm'
        db.create_table(u'repository_accountingfirm', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_cn', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('short_name_cn', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('short_name_en', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('is_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'repository', ['AccountingFirm'])

        # Adding model 'ListedCompany'
        db.create_table(u'repository_listedcompany', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_cn', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('short_name_cn', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('short_name_en', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('intro_cn', self.gf('django.db.models.fields.TextField')(null=True)),
            ('intro_en', self.gf('django.db.models.fields.TextField')(null=True)),
            ('investment_experience_cn', self.gf('django.db.models.fields.TextField')(null=True)),
            ('investment_experience_en', self.gf('django.db.models.fields.TextField')(null=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.Country'])),
            ('province', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.Province'])),
            ('industry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['industry.Industry'])),
            ('address_cn', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('address_en', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('tel', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('stock_exchange', self.gf('django.db.models.fields.related.ForeignKey')(related_name='listed_company_stock_exchange', to=orm['repository.StockExchange'])),
            ('stock_symbol', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'repository', ['ListedCompany'])

        # Adding model 'StockExchange'
        db.create_table(u'repository_stockexchange', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_cn', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'repository', ['StockExchange'])


    def backwards(self, orm):
        # Deleting model 'AccountingFirm'
        db.delete_table(u'repository_accountingfirm')

        # Deleting model 'ListedCompany'
        db.delete_table(u'repository_listedcompany')

        # Deleting model 'StockExchange'
        db.delete_table(u'repository_stockexchange')


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
            'address_cn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Country']"}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['industry.Industry']"}),
            'intro_cn': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'intro_en': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'investment_experience_cn': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'investment_experience_en': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Province']"}),
            'short_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'stock_exchange': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'listed_company_stock_exchange'", 'to': u"orm['repository.StockExchange']"}),
            'stock_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'repository.stockexchange': {
            'Meta': {'object_name': 'StockExchange'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['repository']