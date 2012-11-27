# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'StoreAddress'
        db.create_table('stores_storeaddress', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('line1', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('line2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('line3', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('line4', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('postcode', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['address.Country'])),
            ('search_text', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('store', self.gf('django.db.models.fields.related.OneToOneField')(related_name='address', unique=True, to=orm['stores.Store'])),
        ))
        db.send_create_signal('stores', ['StoreAddress'])

        # Adding model 'StoreGroup'
        db.create_table('stores_storegroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=100, blank=True)),
        ))
        db.send_create_signal('stores', ['StoreGroup'])

        # Adding model 'StoreContact'
        db.create_table('stores_storecontact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('manager_name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            (u'Store', self.gf('django.db.models.fields.related.OneToOneField')(related_name='contact_details', unique=True, to=orm['stores.Store'])),
        ))
        db.send_create_signal('stores', ['StoreContact'])

        # Adding model 'Store'
        db.create_table('stores_store', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, unique=True, null=True)),
            ('reference', self.gf('django.db.models.fields.CharField')(max_length=32, unique=True, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=2000, null=True, blank=True)),
            ('location', self.gf('django.contrib.gis.db.models.fields.PointField')(null=True, blank=True)),
            (u'Group', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='stores', null=True, to=orm['stores.StoreGroup'])),
            ('is_pickup_store', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('stores', ['Store'])

        # Adding model 'OpeningPeriod'
        db.create_table('stores_openingperiod', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'Store', self.gf('django.db.models.fields.related.ForeignKey')(related_name='opening_periods', to=orm['stores.Store'])),
            ('weekday', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('start', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
        ))
        db.send_create_signal('stores', ['OpeningPeriod'])


    def backwards(self, orm):
        # Deleting model 'StoreAddress'
        db.delete_table('stores_storeaddress')

        # Deleting model 'StoreGroup'
        db.delete_table('stores_storegroup')

        # Deleting model 'StoreContact'
        db.delete_table('stores_storecontact')

        # Deleting model 'Store'
        db.delete_table('stores_store')

        # Deleting model 'OpeningPeriod'
        db.delete_table('stores_openingperiod')


    models = {
        'address.country': {
            'Meta': {'ordering': "('-is_highlighted', 'name')", 'object_name': 'Country'},
            'is_highlighted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_shipping_country': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'iso_3166_1_a2': ('django.db.models.fields.CharField', [], {'max_length': '2', 'primary_key': 'True'}),
            'iso_3166_1_a3': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'db_index': 'True'}),
            'iso_3166_1_numeric': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'printable_name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'stores.openingperiod': {
            'Meta': {'ordering': "['weekday']", 'object_name': 'OpeningPeriod'},
            u'Store': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'opening_periods'", 'to': "orm['stores.Store']"}),
            'end': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'start': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'weekday': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'stores.store': {
            u'Group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'stores'", 'null': 'True', 'to': "orm['stores.StoreGroup']"}),
            'Meta': {'object_name': 'Store'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_pickup_store': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'location': ('django.contrib.gis.db.models.fields.PointField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'reference': ('django.db.models.fields.CharField', [], {'max_length': '32', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'null': 'True'})
        },
        'stores.storeaddress': {
            'Meta': {'object_name': 'StoreAddress'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['address.Country']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'line1': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'line2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'line3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'line4': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'search_text': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'store': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'address'", 'unique': 'True', 'to': "orm['stores.Store']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'stores.storecontact': {
            'Meta': {'object_name': 'StoreContact'},
            u'Store': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'contact_details'", 'unique': 'True', 'to': "orm['stores.Store']"}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
        'stores.storegroup': {
            'Meta': {'object_name': 'StoreGroup'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['stores']