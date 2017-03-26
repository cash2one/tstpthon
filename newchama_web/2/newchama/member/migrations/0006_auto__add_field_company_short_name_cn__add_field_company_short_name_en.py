# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Company.short_name_cn'
        db.add_column(u'member_company', 'short_name_cn',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)

        # Adding field 'Company.short_name_en'
        db.add_column(u'member_company', 'short_name_en',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)

        # Adding field 'Company.intro_cn'
        db.add_column(u'member_company', 'intro_cn',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Company.intro_en'
        db.add_column(u'member_company', 'intro_en',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Company.investment_experience_cn'
        db.add_column(u'member_company', 'investment_experience_cn',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Company.investment_experience_en'
        db.add_column(u'member_company', 'investment_experience_en',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Company.intro_file'
        db.add_column(u'member_company', 'intro_file',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True),
                      keep_default=False)

        # Adding field 'Company.updated'
        db.add_column(u'member_company', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 8, 8, 0, 0), blank=True),
                      keep_default=False)


        # Changing field 'Company.name_cn'
        db.alter_column(u'member_company', 'name_cn', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Company.logo'
        db.alter_column(u'member_company', 'logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True))

        # Changing field 'Company.name_en'
        db.alter_column(u'member_company', 'name_en', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))
        # Deleting field 'Member.position'
        db.delete_column(u'member_member', 'position')

        # Adding field 'Member.position_cn'
        db.add_column(u'member_member', 'position_cn',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=20),
                      keep_default=False)

        # Adding field 'Member.position_en'
        db.add_column(u'member_member', 'position_en',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=50),
                      keep_default=False)

        # Adding field 'Member.intro_cn'
        db.add_column(u'member_member', 'intro_cn',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Member.intro_en'
        db.add_column(u'member_member', 'intro_en',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Member.last_login_time'
        db.add_column(u'member_member', 'last_login_time',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'Member.login_count'
        db.add_column(u'member_member', 'login_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Member.avatar'
        db.add_column(u'member_member', 'avatar',
                      self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Company.short_name_cn'
        db.delete_column(u'member_company', 'short_name_cn')

        # Deleting field 'Company.short_name_en'
        db.delete_column(u'member_company', 'short_name_en')

        # Deleting field 'Company.intro_cn'
        db.delete_column(u'member_company', 'intro_cn')

        # Deleting field 'Company.intro_en'
        db.delete_column(u'member_company', 'intro_en')

        # Deleting field 'Company.investment_experience_cn'
        db.delete_column(u'member_company', 'investment_experience_cn')

        # Deleting field 'Company.investment_experience_en'
        db.delete_column(u'member_company', 'investment_experience_en')

        # Deleting field 'Company.intro_file'
        db.delete_column(u'member_company', 'intro_file')

        # Deleting field 'Company.updated'
        db.delete_column(u'member_company', 'updated')


        # Changing field 'Company.name_cn'
        db.alter_column(u'member_company', 'name_cn', self.gf('django.db.models.fields.CharField')(default=None, max_length=255))

        # Changing field 'Company.logo'
        db.alter_column(u'member_company', 'logo', self.gf('django.db.models.fields.files.ImageField')(default=None, max_length=100))

        # Changing field 'Company.name_en'
        db.alter_column(u'member_company', 'name_en', self.gf('django.db.models.fields.CharField')(default=None, max_length=255))
        # Adding field 'Member.position'
        db.add_column(u'member_member', 'position',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=20),
                      keep_default=False)

        # Deleting field 'Member.position_cn'
        db.delete_column(u'member_member', 'position_cn')

        # Deleting field 'Member.position_en'
        db.delete_column(u'member_member', 'position_en')

        # Deleting field 'Member.intro_cn'
        db.delete_column(u'member_member', 'intro_cn')

        # Deleting field 'Member.intro_en'
        db.delete_column(u'member_member', 'intro_en')

        # Deleting field 'Member.last_login_time'
        db.delete_column(u'member_member', 'last_login_time')

        # Deleting field 'Member.login_count'
        db.delete_column(u'member_member', 'login_count')

        # Deleting field 'Member.avatar'
        db.delete_column(u'member_member', 'avatar')


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
            'address_cn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'address_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Country']"}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['industry.Industry']"}),
            'intro_cn': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'intro_en': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'intro_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True'}),
            'investment_experience_cn': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'investment_experience_en': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Province']"}),
            'short_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'stock_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
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
        }
    }

    complete_apps = ['member']