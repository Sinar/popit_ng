# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('popit', '0008_auto_20150930_0137'),
    ]

    operations = [
        migrations.CreateModel(
            name='Citation',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('field_name', models.CharField(max_length=25)),
                ('object_id', models.CharField(max_length=255)),
                ('url', models.URLField()),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CitationTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('notes', models.TextField()),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translated', editable=False, to='popit.Citation', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'popit_citation_translation',
                'db_tablespace': '',
            },
        ),
        migrations.AlterUniqueTogether(
            name='citationtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
