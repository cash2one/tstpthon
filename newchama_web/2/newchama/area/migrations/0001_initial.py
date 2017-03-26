# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Continent'
        db.create_table('area_continent', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name_cn', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'area', ['Continent'])

        # Adding model 'Country'
        db.create_table('area_country', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('continent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.Continent'])),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name_cn', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'area', ['Country'])

        # Adding model 'Province'
        db.create_table('area_province', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.Country'])),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name_cn', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'area', ['Province'])

        # Adding model 'City'
        db.create_table('area_city', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('province', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['area.Province'])),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('name_cn', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'area', ['City'])


    def backwards(self, orm):
        # Deleting model 'Continent'
        db.delete_table('area_continent')

        # Deleting model 'Country'
        db.delete_table('area_country')

        # Deleting model 'Province'
        db.delete_table('area_province')

        # Deleting model 'City'
        db.delete_table('area_city')


    models = {
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
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'area.province': {
            'Meta': {'object_name': 'Province'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['area.Country']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name_cn': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['area']