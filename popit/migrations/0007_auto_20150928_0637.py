# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0006_auto_20150928_0611'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherNames',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('start_date', models.DateField(null=True)),
                ('start_date_source', models.CharField(max_length=255, null=True)),
                ('end_date', models.DateField(null=True)),
                ('end_date_source', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('note', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OtherNamesTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('name_source', models.CharField(max_length=255)),
                ('family_name', models.CharField(max_length=255, null=True)),
                ('family_name_source', models.CharField(max_length=255, null=True)),
                ('given_name', models.CharField(max_length=255, null=True)),
                ('given_name_source', models.CharField(max_length=255, null=True)),
                ('additional_name', models.CharField(max_length=255, null=True)),
                ('add_name_source', models.CharField(max_length=255, null=True)),
                ('honor_prefix', models.CharField(max_length=255, null=True)),
                ('honor_prefix_source', models.CharField(max_length=255, null=True)),
                ('honor_suffix', models.CharField(max_length=255, null=True)),
                ('honor_suffix_source', models.CharField(max_length=255, null=True)),
                ('patronymic_name', models.CharField(max_length=255, null=True)),
                ('patron_name_source', models.CharField(max_length=255, null=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='popit.OtherNames', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'popit_othernames_translation',
                'db_tablespace': '',
            },
        ),
        migrations.AlterUniqueTogether(
            name='othernamestranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
