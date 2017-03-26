# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Project.name'
        db.delete_column(u'project_project', 'name')

        # Adding field 'Project.name_cn'
        db.add_column(u'project_project', 'name_cn',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255),
                      keep_default=False)

        # Adding field 'Project.name_en'
        db.add_column(u'project_project', 'name_en',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255),
                      keep_default=False)

        # Adding field 'Project.status'
        db.add_column(u'project_project', 'status',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Project.pv'
        db.add_column(u'project_project', 'pv',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Project.service_type'
        db.add_column(u'project_project', 'service_type',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Project.price_min'
        db.add_column(u'project_project', 'price_min',
                      self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=10, decimal_places=2),
                      keep_default=False)

        # Adding field 'Project.price_max'
        db.add_column(u'project_project', 'price_max',
                      self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=10, decimal_places=2),
                      keep_default=False)

        # Adding field 'Project.lock_date'
        db.add_column(u'project_project', 'lock_date',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding field 'Project.intro'
        db.add_column(u'project_project', 'intro',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Project.currency_type_service'
        db.add_column(u'project_project', 'currency_type_service',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Project.company_symbol'
        db.add_column(u'project_project', 'company_symbol',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
                      keep_default=False)

        # Adding field 'Project.company_name'
        db.add_column(u'project_project', 'company_name',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)

        # Adding field 'Project.company_country'
        db.add_column(u'project_project', 'company_country',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.Country'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Project.company_province'
        db.add_column(u'project_project', 'company_province',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.Province'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Project.company_industry'
        db.add_column(u'project_project', 'company_industry',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='company_industry', null=True, to=orm['industry.Industry']),
                      keep_default=False)

        # Adding field 'Project.company_stock_symbol'
        db.add_column(u'project_project', 'company_stock_symbol',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True),
                      keep_default=False)

        # Adding field 'Project.financial_is_audit'
        db.add_column(u'project_project', 'financial_is_audit',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Project.financial_audit_company_name'
        db.add_column(u'project_project', 'financial_audit_company_name',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255),
                      keep_default=False)

        # Adding field 'Project.financial_audit_company_is_default'
        db.add_column(u'project_project', 'financial_audit_company_is_default',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Project.currency_type_financial'
        db.add_column(u'project_project', 'currency_type_financial',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Project.financial_year'
        db.add_column(u'project_project', 'financial_year',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Project.income'
        db.add_column(u'project_project', 'income',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2),
                      keep_default=False)

        # Adding field 'Project.profit'
        db.add_column(u'project_project', 'profit',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2),
                      keep_default=False)

        # Adding field 'Project.growth_three_year'
        db.add_column(u'project_project', 'growth_three_year',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Project.employees_count_type'
        db.add_column(u'project_project', 'employees_count_type',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Project.registered_capital'
        db.add_column(u'project_project', 'registered_capital',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Project.total_assets_last_phase'
        db.add_column(u'project_project', 'total_assets_last_phase',
                      self.gf('django.db.models.fields.DecimalField')(default=0, null=True, max_digits=10, decimal_places=2),
                      keep_default=False)

        # Adding field 'Project.income_last_phase'
        db.add_column(u'project_project', 'income_last_phase',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2),
                      keep_default=False)

        # Adding field 'Project.profit_last_phase'
        db.add_column(u'project_project', 'profit_last_phase',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2),
                      keep_default=False)

        # Adding field 'Project.holding_type'
        db.add_column(u'project_project', 'holding_type',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Project.features_cn'
        db.add_column(u'project_project', 'features_cn',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Project.features_en'
        db.add_column(u'project_project', 'features_en',
                      self.gf('django.db.models.fields.TextField')(null=True),
                      keep_default=False)

        # Adding field 'Project.expire_date'
        db.add_column(u'project_project', 'expire_date',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding M2M table for field target_members on 'Project'
        m2m_table_name = db.shorten_name(u'project_project_target_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'project.project'], null=False)),
            ('member', models.ForeignKey(orm[u'member.member'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'member_id'])

        # Adding M2M table for field target_industries on 'Project'
        m2m_table_name = db.shorten_name(u'project_project_target_industries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'project.project'], null=False)),
            ('industry', models.ForeignKey(orm[u'industry.industry'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'industry_id'])


    def backwards(self, orm):
        # Adding field 'Project.name'
        db.add_column(u'project_project', 'name',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=255),
                      keep_default=False)

        # Deleting field 'Project.name_cn'
        db.delete_column(u'project_project', 'name_cn')

        # Deleting field 'Project.name_en'
        db.delete_column(u'project_project', 'name_en')

        # Deleting field 'Project.status'
        db.delete_column(u'project_project', 'status')

        # Deleting field 'Project.pv'
        db.delete_column(u'project_project', 'pv')

        # Deleting field 'Project.service_type'
        db.delete_column(u'project_project', 'service_type')

        # Deleting field 'Project.price_min'
        db.delete_column(u'project_project', 'price_min')

        # Deleting field 'Project.price_max'
        db.delete_column(u'project_project', 'price_max')

        # Deleting field 'Project.lock_date'
        db.delete_column(u'project_project', 'lock_date')

        # Deleting field 'Project.intro'
        db.delete_column(u'project_project', 'intro')

        # Deleting field 'Project.currency_type_service'
        db.delete_column(u'project_project', 'currency_type_service')

        # Deleting field 'Project.company_symbol'
        db.delete_column(u'project_project', 'company_symbol')

        # Deleting field 'Project.company_name'
        db.delete_column(u'project_project', 'company_name')

        # Deleting field 'Project.company_country'
        db.delete_column(u'project_project', 'company_country_id')

        # Deleting field 'Project.company_province'
        db.delete_column(u'project_project', 'company_province_id')

        # Deleting field 'Project.company_industry'
        db.delete_column(u'project_project', 'company_industry_id')

        # Deleting field 'Project.company_stock_symbol'
        db.delete_column(u'project_project', 'company_stock_symbol')

        # Deleting field 'Project.financial_is_audit'
        db.delete_column(u'project_project', 'financial_is_audit')

        # Deleting field 'Project.financial_audit_company_name'
        db.delete_column(u'project_project', 'financial_audit_company_name')

        # Deleting field 'Project.financial_audit_company_is_default'
        db.delete_column(u'project_project', 'financial_audit_company_is_default')

        # Deleting field 'Project.currency_type_financial'
        db.delete_column(u'project_project', 'currency_type_financial')

        # Deleting field 'Project.financial_year'
        db.delete_column(u'project_project', 'financial_year')

        # Deleting field 'Project.income'
        db.delete_column(u'project_project', 'income')

        # Deleting field 'Project.profit'
        db.delete_column(u'project_project', 'profit')

        # Deleting field 'Project.growth_three_year'
        db.delete_column(u'project_project', 'growth_three_year')

        # Deleting field 'Project.employees_count_type'
        db.delete_column(u'project_project', 'employees_count_type')

        # Deleting field 'Project.registered_capital'
        db.delete_column(u'project_project', 'registered_capital')

        # Deleting field 'Project.total_assets_last_phase'
        db.delete_column(u'project_project', 'total_assets_last_phase')

        # Deleting field 'Project.income_last_phase'
        db.delete_column(u'project_project', 'income_last_phase')

        # Deleting field 'Project.profit_last_phase'
        db.delete_column(u'project_project', 'profit_last_phase')

        # Deleting field 'Project.holding_type'
        db.delete_column(u'project_project', 'holding_type')

        # Deleting field 'Project.features_cn'
        db.delete_column(u'project_project', 'features_cn')

        # Deleting field 'Project.features_en'
        db.delete_column(u'project_project', 'features_en')

        # Deleting field 'Project.expire_date'
        db.delete_column(u'project_project', 'expire_date')

        # Removing M2M table for field target_members on 'Project'
        db.delete_table(db.shorten_name(u'project_project_target_members'))

        # Removing M2M table for field target_industries on 'Project'
        db.delete_table(db.shorten_name(u'project_project_target_industries'))


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
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Province']"}),
            'stock_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'member.member': {
            'Meta': {'object_name': 'Member'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member.Company']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'expire_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'gender': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invite_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'invite_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member.Member']", 'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'project.project': {
            'Meta': {'object_name': 'Project'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'company_country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Country']", 'null': 'True', 'blank': 'True'}),
            'company_industry': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'company_industry'", 'null': 'True', 'to': u"orm['industry.Industry']"}),
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
            'financial_audit_company_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'financial_is_audit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'financial_year': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'growth_three_year': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'holding_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'income': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'income_last_phase': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'intro': ('django.db.models.fields.TextField', [], {'null': 'True'}),
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
            'target_industries': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'target_industries'", 'symmetrical': 'False', 'to': u"orm['industry.Industry']"}),
            'target_members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'target_members'", 'symmetrical': 'False', 'to': u"orm['member.Member']"}),
            'total_assets_last_phase': ('django.db.models.fields.DecimalField', [], {'default': '0', 'null': 'True', 'max_digits': '10', 'decimal_places': '2'})
        }
    }

    complete_apps = ['project']