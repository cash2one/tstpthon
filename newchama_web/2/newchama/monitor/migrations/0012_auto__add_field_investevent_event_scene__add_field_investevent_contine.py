# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'InvestEvent.event_scene'
        db.add_column(u'monitor_investevent', 'event_scene',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'InvestEvent.continent'
        db.add_column(u'monitor_investevent', 'continent',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)

        # Adding field 'InvestEvent.country'
        db.add_column(u'monitor_investevent', 'country',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)

        # Adding field 'InvestEvent.province'
        db.add_column(u'monitor_investevent', 'province',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)

        # Adding field 'InvestEvent.city'
        db.add_column(u'monitor_investevent', 'city',
                      self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field cv1 on 'InvestEvent'
        m2m_table_name = db.shorten_name(u'monitor_investevent_cv1')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('investevent', models.ForeignKey(orm[u'monitor.investevent'], null=False)),
            ('industry', models.ForeignKey(orm[u'industry.industry'], null=False))
        ))
        db.create_unique(m2m_table_name, ['investevent_id', 'industry_id'])

        # Adding M2M table for field cv2 on 'InvestEvent'
        m2m_table_name = db.shorten_name(u'monitor_investevent_cv2')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('investevent', models.ForeignKey(orm[u'monitor.investevent'], null=False)),
            ('industry', models.ForeignKey(orm[u'industry.industry'], null=False))
        ))
        db.create_unique(m2m_table_name, ['investevent_id', 'industry_id'])

        # Adding M2M table for field cv3 on 'InvestEvent'
        m2m_table_name = db.shorten_name(u'monitor_investevent_cv3')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('investevent', models.ForeignKey(orm[u'monitor.investevent'], null=False)),
            ('industry', models.ForeignKey(orm[u'industry.industry'], null=False))
        ))
        db.create_unique(m2m_table_name, ['investevent_id', 'industry_id'])


        # Changing field 'InvestEvent.scale'
        db.alter_column(u'monitor_investevent', 'scale', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'InvestEvent.currency'
        db.alter_column(u'monitor_investevent', 'currency', self.gf('django.db.models.fields.IntegerField')())

        # Changing field 'InvestEvent.invest_phase'
        db.alter_column(u'monitor_investevent', 'invest_phase', self.gf('django.db.models.fields.IntegerField')())

    def backwards(self, orm):
        # Deleting field 'InvestEvent.event_scene'
        db.delete_column(u'monitor_investevent', 'event_scene')

        # Deleting field 'InvestEvent.continent'
        db.delete_column(u'monitor_investevent', 'continent')

        # Deleting field 'InvestEvent.country'
        db.delete_column(u'monitor_investevent', 'country')

        # Deleting field 'InvestEvent.province'
        db.delete_column(u'monitor_investevent', 'province')

        # Deleting field 'InvestEvent.city'
        db.delete_column(u'monitor_investevent', 'city')

        # Removing M2M table for field cv1 on 'InvestEvent'
        db.delete_table(db.shorten_name(u'monitor_investevent_cv1'))

        # Removing M2M table for field cv2 on 'InvestEvent'
        db.delete_table(db.shorten_name(u'monitor_investevent_cv2'))

        # Removing M2M table for field cv3 on 'InvestEvent'
        db.delete_table(db.shorten_name(u'monitor_investevent_cv3'))


        # Changing field 'InvestEvent.scale'
        db.alter_column(u'monitor_investevent', 'scale', self.gf('django.db.models.fields.CharField')(max_length=20))

        # Changing field 'InvestEvent.currency'
        db.alter_column(u'monitor_investevent', 'currency', self.gf('django.db.models.fields.CharField')(max_length=10))

        # Changing field 'InvestEvent.invest_phase'
        db.alter_column(u'monitor_investevent', 'invest_phase', self.gf('django.db.models.fields.CharField')(max_length=20))

    models = {
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
        u'monitor.hknotice': {
            'Meta': {'object_name': 'HkNotice'},
            'content': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stock_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'types': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['monitor.HkNoticeType']", 'symmetrical': 'False'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'monitor.hknoticetype': {
            'Meta': {'object_name': 'HkNoticeType'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'notice_type_name': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True'}),
            'parent_id': ('django.db.models.fields.IntegerField', [], {'null': 'True'})
        },
        u'monitor.investevent': {
            'Meta': {'object_name': 'InvestEvent'},
            'amount': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'continent': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'currency': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'cv1': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'cv1'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['industry.Industry']"}),
            'cv2': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'cv2'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['industry.Industry']"}),
            'cv3': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'cv3'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['industry.Industry']"}),
            'data_source': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True'}),
            'event_scene': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introduction': ('django.db.models.fields.TextField', [], {}),
            'invest_phase': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'investee_abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'investee_fullname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'investors': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'scale': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'source_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '40'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'website_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'monitor.shanghaishenzhennotice': {
            'Meta': {'object_name': 'ShanghaiShenzhenNotice'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitor.StockMarket']", 'null': 'True', 'blank': 'True'}),
            'notice_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitor.ShanghaiShenzhenNoticeType']", 'null': 'True', 'blank': 'True'}),
            'pdf_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'published_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        u'monitor.shanghaishenzhennoticetype': {
            'Meta': {'object_name': 'ShanghaiShenzhenNoticeType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'type_name': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'})
        },
        u'monitor.stockmarket': {
            'Meta': {'object_name': 'StockMarket'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'market_name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'symbol': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['monitor']