# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Deal'
        db.create_table('cvsource_deals', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('deal_type', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('amount_usd', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=19, decimal_places=6)),
            ('currency', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('equity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('happen_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('country_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('province_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('city_id', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('target_company', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('cv1', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cv2', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('cv3', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('market_value', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('update_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('add_time', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'deal', ['Deal'])

        # Adding model 'ListDeal'
        db.create_table('cvsource_deals_list', (
            (u'deal_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deal.Deal'], unique=True, primary_key=True)),
            ('list_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('stock_code', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('stock_exchange', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('list_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('list_status', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('advisor_firm', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
            ('acc_firm', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
            ('law_firm', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
        ))
        db.send_create_signal(u'deal', ['ListDeal'])

        # Adding model 'TransDeal'
        db.create_table('cvsource_deals_trans', (
            (u'deal_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deal.Deal'], unique=True, primary_key=True)),
            ('invest_company', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
            ('invest_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('invest_stage', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('finance_advisor', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
        ))
        db.send_create_signal(u'deal', ['TransDeal'])

        # Adding model 'BuyTogetherDeal'
        db.create_table('cvsource_deals_buytogether', (
            (u'deal_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['deal.Deal'], unique=True, primary_key=True)),
            ('buy_company', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('buy_company_intro', self.gf('django.db.models.fields.CharField')(max_length=800, null=True, blank=True)),
            ('sale_company', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('sale_company_intro', self.gf('django.db.models.fields.CharField')(max_length=800, null=True, blank=True)),
            ('buy_type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('buy_way', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('attitude_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('dstrict', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('whether_trade', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('pay_style', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('before_equity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('after_equity', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('sales_income', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('total_assets', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('net_assets', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('net_margin', self.gf('django.db.models.fields.BigIntegerField')(null=True, blank=True)),
            ('pe', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('pb', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('ps', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'deal', ['BuyTogetherDeal'])


    def backwards(self, orm):
        # Deleting model 'Deal'
        db.delete_table('cvsource_deals')

        # Deleting model 'ListDeal'
        db.delete_table('cvsource_deals_list')

        # Deleting model 'TransDeal'
        db.delete_table('cvsource_deals_trans')

        # Deleting model 'BuyTogetherDeal'
        db.delete_table('cvsource_deals_buytogether')


    models = {
        u'deal.buytogetherdeal': {
            'Meta': {'object_name': 'BuyTogetherDeal', 'db_table': "'cvsource_deals_buytogether'", '_ormbases': [u'deal.Deal']},
            'after_equity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'attitude_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'before_equity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'buy_company': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'buy_company_intro': ('django.db.models.fields.CharField', [], {'max_length': '800', 'null': 'True', 'blank': 'True'}),
            'buy_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'buy_way': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'deal_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deal.Deal']", 'unique': 'True', 'primary_key': 'True'}),
            'dstrict': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'net_assets': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'net_margin': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pay_style': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'pb': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'pe': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'ps': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sale_company': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'sale_company_intro': ('django.db.models.fields.CharField', [], {'max_length': '800', 'null': 'True', 'blank': 'True'}),
            'sales_income': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'total_assets': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'whether_trade': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'deal.deal': {
            'Meta': {'object_name': 'Deal', 'db_table': "'cvsource_deals'"},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            'amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '19', 'decimal_places': '6'}),
            'amount_usd': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'city_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'country_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'cv1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cv2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cv3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deal_type': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'equity': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'happen_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market_value': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'province_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'target_company': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        u'deal.listdeal': {
            'Meta': {'object_name': 'ListDeal', 'db_table': "'cvsource_deals_list'", '_ormbases': [u'deal.Deal']},
            'acc_firm': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'advisor_firm': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            u'deal_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deal.Deal']", 'unique': 'True', 'primary_key': 'True'}),
            'law_firm': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'list_status': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'list_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'list_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'stock_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'stock_exchange': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'deal.transdeal': {
            'Meta': {'object_name': 'TransDeal', 'db_table': "'cvsource_deals_trans'", '_ormbases': [u'deal.Deal']},
            u'deal_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['deal.Deal']", 'unique': 'True', 'primary_key': 'True'}),
            'finance_advisor': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'invest_company': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'invest_stage': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'invest_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['deal']