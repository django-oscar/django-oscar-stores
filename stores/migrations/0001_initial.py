# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import oscar.models.fields
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
        ('catalogue', '0004_auto_20150217_1710'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpeningPeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weekday', models.PositiveIntegerField(verbose_name='Weekday', choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')])),
                ('start', models.TimeField(help_text="Leaving start and end time empty is displayed as 'Closed'", null=True, verbose_name='Start', blank=True)),
                ('end', models.TimeField(help_text="Leaving start and end time empty is displayed as 'Closed'", null=True, verbose_name='End', blank=True)),
            ],
            options={
                'ordering': ['weekday'],
                'abstract': False,
                'verbose_name': 'Opening period',
                'verbose_name_plural': 'Opening periods',
            },
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(max_length=100, null=True, verbose_name='Slug')),
                ('manager_name', models.CharField(max_length=200, null=True, verbose_name='Manager name', blank=True)),
                ('phone', models.CharField(max_length=64, null=True, verbose_name='Phone', blank=True)),
                ('email', models.CharField(max_length=100, null=True, verbose_name='Email', blank=True)),
                ('reference', models.CharField(null=True, max_length=32, blank=True, help_text='A reference number that uniquely identifies this store', unique=True, verbose_name='Reference')),
                ('image', models.ImageField(upload_to=b'uploads/store-images', null=True, verbose_name='Image', blank=True)),
                ('description', models.CharField(max_length=2000, null=True, verbose_name='Description', blank=True)),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326, verbose_name='Location')),
                ('is_pickup_store', models.BooleanField(default=True, verbose_name='Is pickup store')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StoreAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(blank=True, max_length=64, verbose_name='Title', choices=[(b'Mr', 'Mr'), (b'Miss', 'Miss'), (b'Mrs', 'Mrs'), (b'Ms', 'Ms'), (b'Dr', 'Dr')])),
                ('first_name', models.CharField(max_length=255, verbose_name='First name', blank=True)),
                ('last_name', models.CharField(max_length=255, verbose_name='Last name', blank=True)),
                ('line1', models.CharField(max_length=255, verbose_name='First line of address')),
                ('line2', models.CharField(max_length=255, verbose_name='Second line of address', blank=True)),
                ('line3', models.CharField(max_length=255, verbose_name='Third line of address', blank=True)),
                ('line4', models.CharField(max_length=255, verbose_name='City', blank=True)),
                ('state', models.CharField(max_length=255, verbose_name='State/County', blank=True)),
                ('postcode', oscar.models.fields.UppercaseCharField(max_length=64, verbose_name='Post/Zip-code', blank=True)),
                ('search_text', models.TextField(verbose_name='Search text - used only for searching addresses', editable=False)),
                ('country', models.ForeignKey(verbose_name='Country', to='address.Country')),
                ('store', models.OneToOneField(related_name='address', verbose_name='Store', to='stores.Store')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StoreGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='Name')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='Slug')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StoreStock',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_in_stock', models.PositiveIntegerField(default=0, null=True, verbose_name='Number in stock', blank=True)),
                ('num_allocated', models.IntegerField(default=0, null=True, verbose_name='Number allocated', blank=True)),
                ('location', models.CharField(max_length=50, null=True, verbose_name='In store location', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='Date created')),
                ('date_updated', models.DateTimeField(auto_now=True, verbose_name='Date updated', db_index=True)),
                ('product', models.ForeignKey(related_name='store_stock', verbose_name='Product', to='catalogue.Product')),
                ('store', models.ForeignKey(related_name='stock', verbose_name='Store', to='stores.Store')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Store stock record',
                'verbose_name_plural': 'Store stock records',
            },
        ),
        migrations.AddField(
            model_name='store',
            name='group',
            field=models.ForeignKey(related_name='stores', verbose_name='Group', blank=True, to='stores.StoreGroup', null=True),
        ),
        migrations.AddField(
            model_name='openingperiod',
            name='store',
            field=models.ForeignKey(related_name='opening_periods', verbose_name='Store', to='stores.Store'),
        ),
        migrations.AlterUniqueTogether(
            name='storestock',
            unique_together=set([('store', 'product')]),
        ),
    ]
