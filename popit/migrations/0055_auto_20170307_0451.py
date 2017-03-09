# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-07 04:51
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0054_auto_20170307_0122'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.CharField(blank=True, max_length=255, primary_key=True, serialize=False)),
                ('start_date', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(b'^[0-9]{4}(-[0-9]{2}){0,2}$')], verbose_name='start date')),
                ('end_date', models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(b'^[0-9]{4}(-[0-9]{2}){0,2}$')], verbose_name='end date')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('object', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subjects', to='popit.Person', verbose_name='object')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='objects', to='popit.Person', verbose_name='subject')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RelationTranslation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, max_length=255, null=True, verbose_name='Label')),
                ('language_code', models.CharField(db_index=True, max_length=15)),
                ('master', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='translated', to='popit.Relation')),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'popit_relation_translation',
                'db_tablespace': '',
                'default_permissions': (),
            },
        ),
        migrations.AlterUniqueTogether(
            name='relationtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
