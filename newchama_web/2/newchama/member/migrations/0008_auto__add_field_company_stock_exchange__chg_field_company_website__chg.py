# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Company.stock_exchange'
        db.add_column(u'member_company', 'stock_exchange',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['repository.StockExchange'], null=True, blank=True),
                      keep_default=False)


        # Changing field 'Company.website'
        db.alter_column(u'member_company', 'website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

        # Changing field 'Company.tel'
        db.alter_column(u'member_company', 'tel', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'Company.postcode'
        db.alter_column(u'member_company', 'postcode', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'Company.address_en'
        db.alter_column(u'member_company', 'address_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Company.stock_symbol'
        db.alter_column(u'member_company', 'stock_symbol', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'Company.province'
        db.alter_column(u'member_company', 'province_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.Province'], null=True))

        # Changing field 'Company.fax'
        db.alter_column(u'member_company', 'fax', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'Company.country'
        db.alter_column(u'member_company', 'country_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.Country'], null=True))

        # Changing field 'Company.industry'
        db.alter_column(u'member_company', 'industry_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['industry.Industry'], null=True))

        # Changing field 'Company.address_cn'
        db.alter_column(u'member_company', 'address_cn', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):
        # Deleting field 'Company.stock_exchange'
        db.delete_column(u'member_company', 'stock_exchange_id')


        # Changing field 'Company.website'
        db.alter_column(u'member_company', 'website', self.gf('django.db.models.fields.URLField')(default=None, max_length=200))

        # Changing field 'Company.tel'
        db.alter_column(u'member_company', 'tel', self.gf('django.db.models.fields.CharField')(default=None, max_length=20))

        # Changing field 'Company.postcode'
        db.alter_column(u'member_company', 'postcode', self.gf('django.db.models.fields.CharField')(default=None, max_length=20))

        # Changing field 'Company.address_en'
        db.alter_column(u'member_company', 'address_en', self.gf('django.db.models.fields.CharField')(default=None, max_length=255))

        # Changing field 'Company.stock_symbol'
        db.alter_column(u'member_company', 'stock_symbol', self.gf('django.db.models.fields.CharField')(default=None, max_length=20))

        # Changing field 'Company.province'
        db.alter_column(u'member_company', 'province_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['area.Province']))

        # Changing field 'Company.fax'
        db.alter_column(u'member_company', 'fax', self.gf('django.db.models.fields.CharField')(default=None, max_length=20))

        # Changing field 'Company.country'
        db.alter_column(u'member_company', 'country_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['area.Country']))

        # Changing field 'Company.industry'
        db.alter_column(u'member_company', 'industry_id', self.gf('django.db.models.fields.related.ForeignKey')(default=None, to=orm['industry.Industry']))

        # Changing field 'Company.address_cn'
        db.alter_column(u'member_company', 'address_cn', self.gf('django.db.models.fields.CharField')(default=None, max_length=255))

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
        u'member.company': {
            'Meta': {'object_name': 'Company'},
            'address_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'address_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Country']", 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['industry.Industry']", 'null': 'True', 'blank': 'True'}),
            'intro_cn': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'intro_en': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'intro_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'investment_experience_cn': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'investment_experience_en': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Province']", 'null': 'True', 'blank': 'True'}),
            'short_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'stock_exchange': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.StockExchange']", 'null': 'True', 'blank': 'True'}),
            'stock_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        u'member.invitecode': {
            'Meta': {'object_name': 'InviteCode'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member.Member']"}),
            'isused': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'used_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None'})
        },
        u'member.member': {
            'Meta': {'object_name': 'Member'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member.Company']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'expire_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gender': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_cn': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'intro_en': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'invite_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'invite_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member.Member']", 'null': 'True', 'blank': 'True'}),
            'last_login_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'login_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'position_cn': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'position_en': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'member.message': {
            'Meta': {'object_name': 'Message'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_delete': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'is_read': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'receiver': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'member_receiver'", 'to': u"orm['member.Member']"}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'member_sender'", 'to': u"orm['member.Member']"})
        },
        u'repository.stockexchange': {
            'Meta': {'object_name': 'StockExchange'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['member']