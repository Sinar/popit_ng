# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0005_contacts_updated_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Identifiers',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('identifier', models.CharField(max_length=255)),
                ('sources', models.CharField(max_length=255)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IdentifiersTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('scheme', models.CharField(max_length=255)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='popit.Identifiers', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'popit_identifiers_translation',
                'db_tablespace': '',
            },
        ),
        migrations.AlterUniqueTogether(
            name='identifierstranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
