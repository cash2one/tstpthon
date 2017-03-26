# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Project.create_source'
        db.add_column('project_project', 'create_source',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Project.multi_currency'
        db.add_column('project_project', 'multi_currency',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Project.create_source'
        db.delete_column('project_project', 'create_source')

        # Deleting field 'Project.multi_currency'
        db.delete_column('project_project', 'multi_currency')


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
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sort': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
        u'member.buyerdealcategory': {
            'Meta': {'object_name': 'BuyerDealCategory'},
            'category': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
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
            'investment_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'is_list': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'memo': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'new_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'parent_company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member.Company']", 'null': 'True', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Province']", 'null': 'True', 'blank': 'True'}),
            'short_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 18, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'member.detaildealtype': {
            'Meta': {'object_name': 'DetailDealType'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'deal_types'", 'to': u"orm['member.BuyerDealCategory']"}),
            'deal_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'seller_category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'seller_deal_types'", 'null': 'True', 'to': u"orm['member.SellerDealCategory']"})
        },
        u'member.member': {
            'Meta': {'object_name': 'Member'},
            'activecode': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'avatar': ('django.db.models.fields.files.ImageField', [], {'default': "'default.jpg'", 'max_length': '100', 'blank': 'True'}),
            'company': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member.Company']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'creator'", 'null': 'True', 'to': u"orm['adminuser.AdminUser']"}),
            'deal_currency': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'deal_size_max': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'deal_size_min': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'expire_date': ('django.db.models.fields.DateField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'focus_aspect': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['industry.Industry']", 'symmetrical': 'False'}),
            'focus_investor_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member.BuyerDealCategory']", 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intro_cn': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'intro_en': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'investment': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'invite_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'invite_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['member.Member']", 'null': 'True', 'blank': 'True'}),
            'is_subscribe_push': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'last_login_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'linkedin': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'linkedin'", 'null': 'True', 'to': u"orm['member.OtherLogin']"}),
            'login_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'mobile_intel': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'not_push_reason': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owner'", 'null': 'True', 'to': u"orm['adminuser.AdminUser']"}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'position_cn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'position_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'role': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'tel_intel': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'weibo': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'weibo'", 'null': 'True', 'to': u"orm['member.OtherLogin']"}),
            'weibo_url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'weixin': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'weixin'", 'null': 'True', 'to': u"orm['member.OtherLogin']"})
        },
        u'member.otherlogin': {
            'Meta': {'object_name': 'OtherLogin', 'db_table': "'other_login'"},
            'access_token': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'expires_in': ('django.db.models.fields.BigIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'uid': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        u'member.sellerdealcategory': {
            'Meta': {'object_name': 'SellerDealCategory'},
            'category': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        },
        u'project.project': {
            'Meta': {'object_name': 'Project'},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'audit_status': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'audit_status_2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'audit_status_3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'company_cities': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.City']", 'null': 'True', 'blank': 'True'}),
            'company_country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Country']", 'null': 'True', 'blank': 'True'}),
            'company_industry': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'project_company_industry'", 'null': 'True', 'to': u"orm['industry.Industry']"}),
            'company_industry_intro_cn': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'company_industry_intro_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'company_intro_cn': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'company_intro_en': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'company_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'company_name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'company_province': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Province']", 'null': 'True', 'blank': 'True'}),
            'company_stock_exchange': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['repository.StockExchange']", 'null': 'True', 'blank': 'True'}),
            'company_stock_symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'company_symbol_cn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'company_symbol_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'create_source': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'currency_type_financial': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'currency_type_service': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cv1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cv2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cv3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deal_size': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deal_type': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['member.DetailDealType']", 'symmetrical': 'False'}),
            'ebitda': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'ebitda_2': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'ebitda_3': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'employees_count_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'expected_enterprice_value': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'expire_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'features_cn': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'features_en': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'financial_audit_company_is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'financial_audit_company_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'financial_is_audit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'financial_year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'growth_three_year': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2'}),
            'has_attach': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'income': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'income_last_phase': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'income_last_phase_2': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'income_last_phase_3': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'income_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'integrity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'integrity_en': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'intro_cn': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'intro_en': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'is_agent_project': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_follow': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_list_company': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_recommend': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_suitor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_top': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lock_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'member_publisher'", 'to': u"orm['member.Member']"}),
            'multi_currency': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pay_currency': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'price_max': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'price_min': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'process': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'profit': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'profit_last_phase': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'profit_last_phase_2': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'profit_last_phase_3': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'profit_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'project_relation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'project_stage': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'pv': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'registered_capital': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'service_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'stock_percent': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '6', 'decimal_places': '2', 'blank': 'True'}),
            'target_companies': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['member.Company']", 'symmetrical': 'False'}),
            'target_industries': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['industry.Industry']", 'symmetrical': 'False'}),
            'target_members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['member.Member']", 'symmetrical': 'False'}),
            'total_assets_last_phase': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'total_assets_last_phase_2': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'total_assets_last_phase_3': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'total_profit_last_phase': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'total_profit_last_phase_2': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'total_profit_last_phase_3': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 18, 0, 0)', 'auto_now': 'True', 'blank': 'True'}),
            'upload_file': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'valid_day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'project.projectattach': {
            'Meta': {'object_name': 'ProjectAttach', 'db_table': "'project_projectAttach'"},
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'file_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'file_type_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_attach'", 'to': u"orm['project.Project']"})
        },
        u'project.projectchecklog': {
            'Meta': {'object_name': 'ProjectCheckLog', 'db_table': "'project_check_log'"},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'adminuser': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_check_log_adminuser'", 'to': u"orm['adminuser.AdminUser']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_check_log_project'", 'to': u"orm['project.Project']"}),
            'reason': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'result': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'project.projectcustomertargetcompany': {
            'Meta': {'object_name': 'ProjectCustomerTargetCompany', 'db_table': "'project_customer_target_company'"},
            'company_field': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'company_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'company_logo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'company_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'company_name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'company_short_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'company_short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'company_type': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'has_user': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_delete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_man': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_star': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_customer_target_company'", 'to': u"orm['project.Project']"}),
            'rank': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'target_reason': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'project.projectdownloadlog': {
            'Meta': {'object_name': 'ProjectDownloadLog', 'db_table': "'project_download_log'"},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_download_log_member'", 'to': u"orm['member.Member']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_download_log_project'", 'to': u"orm['project.Project']"})
        },
        u'project.projectkeyword': {
            'Meta': {'object_name': 'ProjectKeyword', 'db_table': "'project_keyword'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_keyword'", 'to': u"orm['project.Project']"})
        },
        u'project.projectkeywordadmin': {
            'Meta': {'object_name': 'ProjectKeywordAdmin', 'db_table': "'project_keyword_Admin'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_keyword_admin'", 'to': u"orm['project.Project']"})
        },
        u'project.projectkeyworden': {
            'Meta': {'object_name': 'ProjectKeywordEn', 'db_table': "'project_keyword_en'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_keyword_en'", 'to': u"orm['project.Project']"})
        },
        u'project.projectoneclickattach': {
            'Meta': {'object_name': 'ProjectOneclickAttach', 'db_table': "'project_oneclickAttach'"},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'file_size': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '16', 'decimal_places': '2', 'blank': 'True'}),
            'file_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'onclick_publisher'", 'to': u"orm['member.Member']"}),
            'new_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_oneclick_attach'", 'null': 'True', 'to': u"orm['project.Project']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 18, 0, 0)', 'auto_now': 'True', 'blank': 'True'})
        },
        u'project.projectothertargetcompany': {
            'Meta': {'object_name': 'ProjectOtherTargetCompany', 'db_table': "'project_other_target_company'"},
            'company_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_other_company'", 'to': u"orm['project.Project']"}),
            'short_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'table_name': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'project.projectprintlog': {
            'Meta': {'object_name': 'ProjectPrintLog', 'db_table': "'project_print_log'"},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_print_log_member'", 'to': u"orm['member.Member']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_print_log_project'", 'to': u"orm['project.Project']"})
        },
        u'project.projectrecommendlog': {
            'Meta': {'object_name': 'ProjectRecommendLog', 'db_table': "'project_recommend_log'"},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_recommend_log_project'", 'to': u"orm['project.Project']"}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'project.projectrecommondreasonadmin': {
            'Meta': {'object_name': 'ProjectRecommondReasonAdmin', 'db_table': "'project_admin_recommond_reason'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_recommond_reason_admin'", 'to': u"orm['project.Project']"}),
            'reason': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'})
        },
        u'project.projecttag': {
            'Meta': {'object_name': 'ProjectTag', 'db_table': "'project_tag'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_tag'", 'to': u"orm['project.Project']"}),
            'tag': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'})
        },
        u'project.projectviewlog': {
            'Meta': {'object_name': 'ProjectViewLog', 'db_table': "'project_view_log'"},
            'add_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'member': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_view_log_member'", 'to': u"orm['member.Member']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_view_log_project'", 'to': u"orm['project.Project']"})
        },
        u'project.stockstructure': {
            'Meta': {'object_name': 'StockStructure'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'project_stock_structure'", 'to': u"orm['project.Project']"}),
            'rate': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '6', 'decimal_places': '2'}),
            'type': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        u'repository.stockexchange': {
            'Meta': {'object_name': 'StockExchange'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'short_name_cn': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'short_name_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['project']