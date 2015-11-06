# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0032_auto_20151021_2344'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, verbose_name='id', primary_key=True, blank=True)),
                ('start_date', models.CharField(max_length=20, null=True, verbose_name='start date', blank=True)),
                ('end_date', models.CharField(max_length=20, null=True, verbose_name='end date', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now_add=True, verbose_name='updated at')),
                ('area', models.ForeignKey(to='popit.Area')),
                ('organization', models.ForeignKey(to='popit.Organization')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PostTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255, verbose_name='label')),
                ('role', models.CharField(max_length=20, null=True, verbose_name='role', blank=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='popit.Post', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'popit_post_translation',
                'db_tablespace': '',
            },
        ),
        migrations.AlterUniqueTogether(
            name='posttranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
