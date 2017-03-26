# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Demand'
        db.create_table(u'demand_demand', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_cn', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('member', self.gf('django.db.models.fields.related.ForeignKey')(related_name='member_demand_publisher', to=orm['member.Member'])),
            ('add_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('pv', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('service_type', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('intro_cn', self.gf('django.db.models.fields.TextField')(null=True)),
            ('intro_en', self.gf('django.db.models.fields.TextField')(null=True)),
            ('business_cn', self.gf('django.db.models.fields.TextField')(null=True)),
            ('business_en', self.gf('django.db.models.fields.TextField')(null=True)),
            ('company_symbol', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('company_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('company_country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.Country'], null=True, blank=True)),
            ('company_province', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.Province'], null=True, blank=True)),
            ('company_industry', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='demand_target_company_industry', null=True, to=orm['industry.Industry'])),
            ('company_stock_symbol', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('financial_is_audit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('financial_audit_company_is_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('currency_type_financial', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('financial_year', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('income', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('profit', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('growth_three_year', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('net_assets', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('employees_count_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('registered_capital', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total_assets_last_phase', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('income_last_phase', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('profit_last_phase', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('holding_type', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('remark_cn', self.gf('django.db.models.fields.TextField')(null=True)),
            ('remark_en', self.gf('django.db.models.fields.TextField')(null=True)),
            ('expire_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('is_anonymous', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'demand', ['Demand'])

        # Adding M2M table for field target_members on 'Demand'
        m2m_table_name = db.shorten_name(u'demand_demand_target_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('demand', models.ForeignKey(orm[u'demand.demand'], null=False)),
            ('member', models.ForeignKey(orm[u'member.member'], null=False))
        ))
        db.create_unique(m2m_table_name, ['demand_id', 'member_id'])

        # Adding M2M table for field target_industries on 'Demand'
        m2m_table_name = db.shorten_name(u'demand_demand_target_industries')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('demand', models.ForeignKey(orm[u'demand.demand'], null=False)),
            ('industry', models.ForeignKey(orm[u'industry.industry'], null=False))
        ))
        db.create_unique(m2m_table_name, ['demand_id', 'industry_id'])


    def backwards(self, orm):
        # Deleting model 'Demand'
        db.delete_table(u'demand_demand')

        # Removing M2M table for field target_members on 'Demand'
        db.delete_table(db.shorten_name(u'demand_demand_target_members'))

        # Removing M2M table for field target_industries on 'Demand'
        db.delete_table(db.shorten_name(u'demand_demand_target_industries'))


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
        u'demand.demand': {
            'Meta': {'object_name': 'Demand'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'business_cn': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'business_en': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'company_country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Country']", 'null': 'True', 'blank': 'True'}),
            'company_industry': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'demand_target_company_industry'", 'null': 'True', 'to': u"orm['industry.Industry']"}),
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'company_province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Province']", 'null': 'True', 'blank': 'True'}),
            'company_stock_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'company_symbol': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'currency_type_financial': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'employees_count_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'expire_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'financial_audit_company_is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'financial_is_audit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'financial_year': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'growth_three_year': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'holding_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'income': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'income_last_phase': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'intro_cn': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'intro_en': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'is_anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'member_demand_publisher'", 'to': u"orm['member.Member']"}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'net_assets': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'profit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'profit_last_phase': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'pv': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'registered_capital': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'remark_cn': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'remark_en': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'service_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'target_industries': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'demand_push_target_industries'", 'symmetrical': 'False', 'to': u"orm['industry.Industry']"}),
            'target_members': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'demand_push_target_members'", 'symmetrical': 'False', 'to': u"orm['member.Member']"}),
            'total_assets_last_phase': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
        }
    }

    complete_apps = ['demand']