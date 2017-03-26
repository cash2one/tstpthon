# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding M2M table for field target_companies on 'Project'
        m2m_table_name = db.shorten_name(u'project_project_target_companies')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'project.project'], null=False)),
            ('company', models.ForeignKey(orm[u'member.company'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'company_id'])


    def backwards(self, orm):
        # Removing M2M table for field target_companies on 'Project'
        db.delete_table(db.shorten_name(u'project_project_target_companies'))


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
        u'project.project': {
            'Meta': {'object_name': 'Project'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'company_country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Country']", 'null': 'True', 'blank': 'True'}),
            'company_industry': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'project_company_industry'", 'null': 'True', 'to': u"orm['industry.Industry']"}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'company_province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Province']", 'null': 'True', 'blank': 'True'}),
            'company_stock_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'company_symbol': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'currency_type_financial': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'currency_type_service': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'employees_count_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'expire_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'features_cn': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'features_en': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'financial_audit_company_is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'financial_audit_company_name': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '255', 'null': 'True'}),
            'financial_is_audit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'financial_year': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'growth_three_year': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'income': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'income_last_phase': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'intro_cn': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'intro_en': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'lock_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'member_publisher'", 'to': u"orm['member.Member']"}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'price_max': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'price_min': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'profit': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'profit_last_phase': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'pv': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'registered_capital': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'service_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'target_companies': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['member.Company']", 'symmetrical': 'False'}),
            'target_industries': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['industry.Industry']", 'symmetrical': 'False'}),
            'target_members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['member.Member']", 'symmetrical': 'False'}),
            'total_assets_last_phase': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'})
        },
        u'project.stockstructure': {
            'Meta': {'object_name': 'StockStructure'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_stock_structure'", 'to': u"orm['project.Project']"}),
            'rate': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'repository.stockexchange': {
            'Meta': {'object_name': 'StockExchange'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['project']