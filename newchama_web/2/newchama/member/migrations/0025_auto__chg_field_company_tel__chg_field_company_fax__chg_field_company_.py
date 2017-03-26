# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Company.tel'
        db.alter_column('member_company', 'tel', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'Company.fax'
        db.alter_column('member_company', 'fax', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'Company.postcode'
        db.alter_column('member_company', 'postcode', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'Company.address_en'
        db.alter_column('member_company', 'address_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Company.name_cn'
        db.alter_column('member_company', 'name_cn', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Company.intro_en'
        db.alter_column('member_company', 'intro_en', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Company.intro_cn'
        db.alter_column('member_company', 'intro_cn', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Company.stock_symbol'
        db.alter_column('member_company', 'stock_symbol', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'Company.website'
        db.alter_column('member_company', 'website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

        # Changing field 'Company.short_name_cn'
        db.alter_column('member_company', 'short_name_cn', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Company.name_en'
        db.alter_column('member_company', 'name_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Company.stock_symbol_no_pre'
        db.alter_column('member_company', 'stock_symbol_no_pre', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'Company.short_name_en'
        db.alter_column('member_company', 'short_name_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Company.investment_experience_en'
        db.alter_column('member_company', 'investment_experience_en', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Company.address_cn'
        db.alter_column('member_company', 'address_cn', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Company.investment_experience_cn'
        db.alter_column('member_company', 'investment_experience_cn', self.gf('django.db.models.fields.TextField')(null=True))

    def backwards(self, orm):

        # Changing field 'Company.tel'
        db.alter_column('member_company', 'tel', self.gf('django.db.models.fields.CharField')(default='', max_length=20))

        # Changing field 'Company.fax'
        db.alter_column('member_company', 'fax', self.gf('django.db.models.fields.CharField')(default='', max_length=20))

        # Changing field 'Company.postcode'
        db.alter_column('member_company', 'postcode', self.gf('django.db.models.fields.CharField')(default='', max_length=20))

        # Changing field 'Company.address_en'
        db.alter_column('member_company', 'address_en', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Company.name_cn'
        db.alter_column('member_company', 'name_cn', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Company.intro_en'
        db.alter_column('member_company', 'intro_en', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Company.intro_cn'
        db.alter_column('member_company', 'intro_cn', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Company.stock_symbol'
        db.alter_column('member_company', 'stock_symbol', self.gf('django.db.models.fields.CharField')(default='', max_length=20))

        # Changing field 'Company.website'
        db.alter_column('member_company', 'website', self.gf('django.db.models.fields.URLField')(default='', max_length=200))

        # Changing field 'Company.short_name_cn'
        db.alter_column('member_company', 'short_name_cn', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Company.name_en'
        db.alter_column('member_company', 'name_en', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Company.stock_symbol_no_pre'
        db.alter_column('member_company', 'stock_symbol_no_pre', self.gf('django.db.models.fields.CharField')(default='', max_length=20))

        # Changing field 'Company.short_name_en'
        db.alter_column('member_company', 'short_name_en', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Company.investment_experience_en'
        db.alter_column('member_company', 'investment_experience_en', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Company.address_cn'
        db.alter_column('member_company', 'address_cn', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Company.investment_experience_cn'
        db.alter_column('member_company', 'investment_experience_cn', self.gf('django.db.models.fields.TextField')(default=''))

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
            'address_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Country']", 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['industry.Industry']", 'null': 'True', 'blank': 'True'}),
            'intro_cn': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'intro_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'intro_file': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'investment_experience_cn': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'investment_experience_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Province']", 'null': 'True', 'blank': 'True'}),
            'short_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'stock_exchange': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.StockExchange']", 'null': 'True', 'db_column': "'stock_exchange_code'", 'blank': 'True'}),
            'stock_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'stock_symbol_no_pre': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 28, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'member.entryform': {
            'Meta': {'object_name': 'EntryForm'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Country']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fullname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'gender': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['industry.Industry']"}),
            'invite_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Province']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'member.findpasswordhistory': {
            'Meta': {'object_name': 'FindPasswordHistory'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_used': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'used_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'member.invitecode': {
            'Meta': {'object_name': 'InviteCode'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member.Member']"}),
            'is_used': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'used_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        },
        u'member.member': {
            'Meta': {'object_name': 'Member'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'default': "'default.jpg'", 'max_length': '100', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member.Company']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'expire_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gender': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_cn': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'intro_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'invite_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'invite_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member.Member']", 'null': 'True', 'blank': 'True'}),
            'last_login_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'login_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position_cn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'position_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
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
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'primary_key': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'short_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['member']