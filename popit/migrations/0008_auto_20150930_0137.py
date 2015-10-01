# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0007_auto_20150928_0637'),
    ]

    operations = [
        migrations.CreateModel(
            name='Persons',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('birth_date', models.CharField(max_length=20, null=True)),
                ('death_date', models.CharField(max_length=20, null=True)),
                ('image', models.CharField(max_length=255, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PersonsTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('family_name', models.CharField(max_length=255, null=True)),
                ('given_name', models.CharField(max_length=255, null=True)),
                ('additional_name', models.CharField(max_length=255, null=True)),
                ('honorific_prefix', models.CharField(max_length=255, null=True)),
                ('honorific_suffix', models.CharField(max_length=255, null=True)),
                ('patronymic_name', models.CharField(max_length=255, null=True)),
                ('sort_name', models.CharField(max_length=255, null=True)),
                ('gender', models.CharField(max_length=25, null=True)),
                ('summary', models.CharField(max_length=255, blank=True)),
                ('biography', models.TextField()),
                ('national_identity', models.CharField(max_length=255)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='popit.Persons', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'popit_persons_translation',
                'db_tablespace': '',
            },
        ),
        migrations.AlterUniqueTogether(
            name='personstranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
