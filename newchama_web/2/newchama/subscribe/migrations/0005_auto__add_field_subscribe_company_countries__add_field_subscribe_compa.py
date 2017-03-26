# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Subscribe.company_countries'
        db.add_column('project_subscribe', 'company_countries',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.Country'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Subscribe.company_provinces'
        db.add_column('project_subscribe', 'company_provinces',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.Province'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Subscribe.company_cities'
        db.add_column('project_subscribe', 'company_cities',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.City'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Subscribe.company_industries'
        db.add_column('project_subscribe', 'company_industries',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['industry.Industry'], null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field company_cities on 'Subscribe'
        db.delete_table(db.shorten_name('project_subscribe_company_cities'))

        # Removing M2M table for field company_provinces on 'Subscribe'
        db.delete_table(db.shorten_name('project_subscribe_company_provinces'))

        # Removing M2M table for field company_industries on 'Subscribe'
        db.delete_table(db.shorten_name('project_subscribe_company_industries'))

        # Removing M2M table for field company_countries on 'Subscribe'
        db.delete_table(db.shorten_name('project_subscribe_company_countries'))


    def backwards(self, orm):
        # Deleting field 'Subscribe.company_countries'
        db.delete_column('project_subscribe', 'company_countries_id')

        # Deleting field 'Subscribe.company_provinces'
        db.delete_column('project_subscribe', 'company_provinces_id')

        # Deleting field 'Subscribe.company_cities'
        db.delete_column('project_subscribe', 'company_cities_id')

        # Deleting field 'Subscribe.company_industries'
        db.delete_column('project_subscribe', 'company_industries_id')

        # Adding M2M table for field company_cities on 'Subscribe'
        m2m_table_name = db.shorten_name('project_subscribe_company_cities')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('subscribe', models.ForeignKey(orm[u'subscribe.subscribe'], null=False)),
            ('city', models.ForeignKey(orm[u'area.city'], null=False))
        ))
        db.create_unique(m2m_table_name, ['subscribe_id', 'city_id'])

        # Adding M2M table for field company_provinces on 'Subscribe'
        m2m_table_name = db.shorten_name('project_subscribe_company_provinces')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('subscribe', models.ForeignKey(orm[u'subscribe.subscribe'], null=False)),
            ('province', models.ForeignKey(orm[u'area.province'], null=False))
        ))
        db.create_unique(m2m_table_name, ['subscribe_id', 'province_id'])

        # Adding M2M table for field company_industries on 'Subscribe'
        m2m_table_name = db.shorten_name('project_subscribe_company_industries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('subscribe', models.ForeignKey(orm[u'subscribe.subscribe'], null=False)),
            ('industry', models.ForeignKey(orm[u'industry.industry'], null=False))
        ))
        db.create_unique(m2m_table_name, ['subscribe_id', 'industry_id'])

        # Adding M2M table for field company_countries on 'Subscribe'
        m2m_table_name = db.shorten_name('project_subscribe_company_countries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('subscribe', models.ForeignKey(orm[u'subscribe.subscribe'], null=False)),
            ('country', models.ForeignKey(orm[u'area.country'], null=False))
        ))
        db.create_unique(m2m_table_name, ['subscribe_id', 'country_id'])


    models = {
        u'adminuser.adminuser': {
            'Meta': {'object_name': 'AdminUser'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isactive': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'realname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'role': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['adminuser.Role']", 'symmetrical': 'False'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'adminuser.role': {
            'Meta': {'object_name': 'Role'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'permission': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
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
            'intel_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
            'is_display': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'member.company': {
            'Meta': {'object_name': 'Company'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'address_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'capital_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.City']", 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Country']", 'null': 'True', 'blank': 'True'}),
            'data_source': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'found_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['industry.Industry']", 'null': 'True', 'blank': 'True'}),
            'intro_cn': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'intro_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'intro_file': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'investment_experience_cn': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'investment_experience_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'memo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parent_company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member.Company']", 'null': 'True', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Province']", 'null': 'True', 'blank': 'True'}),
            'short_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 5, 6, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'member.member': {
            'Meta': {'object_name': 'Member'},
            'activecode': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'default': "'default.jpg'", 'max_length': '100', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'creator'", 'null': 'True', 'to': u"orm['adminuser.AdminUser']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'expire_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'focus_aspect': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['industry.Industry']", 'symmetrical': 'False'}),
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
            'mobile_intel': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owner'", 'null': 'True', 'to': u"orm['adminuser.AdminUser']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position_cn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'position_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'tel_intel': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'subscribe.subscribe': {
            'Meta': {'object_name': 'Subscribe', 'db_table': "'project_subscribe'"},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'company_cities': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.City']", 'null': 'True', 'blank': 'True'}),
            'company_countries': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Country']", 'null': 'True', 'blank': 'True'}),
            'company_industries': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['industry.Industry']", 'null': 'True', 'blank': 'True'}),
            'company_provinces': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Province']", 'null': 'True', 'blank': 'True'}),
            'currency_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cv1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cv2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cv3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deal_size_max': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deal_size_min': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_delete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'member_subscribe_publisher'", 'to': u"orm['member.Member']"}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'project_stage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'service_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'tip_interval': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'total_match': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 5, 6, 0, 0)', 'auto_now': 'True', 'blank': 'True'})
        },
        u'subscribe.subscribekeyword': {
            'Meta': {'object_name': 'SubscribeKeyword', 'db_table': "'project_subscribe_keyword'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'subscribe': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscribe_keyword'", 'to': u"orm['subscribe.Subscribe']"})
        }
    }

    complete_apps = ['subscribe']