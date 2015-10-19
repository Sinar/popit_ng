# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0025_auto_20151019_0145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True, blank=True)),
                ('founding_date', models.CharField(max_length=20, null=True, verbose_name='founding date', blank=True)),
                ('dissolution_date', models.CharField(max_length=20, null=True, verbose_name='dissolution date', blank=True)),
                ('image', models.URLField(null=True, verbose_name='image', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('area', models.ForeignKey(to='popit.Area')),
                ('parent', models.ForeignKey(related_name='children', to='popit.Organization')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrganizationTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('classification', models.CharField(max_length=255, null=True, verbose_name='classification', blank=True)),
                ('abstract', models.CharField(max_length=255, null=True, verbose_name='abstract', blank=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translated', editable=False, to='popit.Organization', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'popit_organization_translation',
                'db_tablespace': '',
            },
        ),
        migrations.AlterUniqueTogether(
            name='organizationtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
