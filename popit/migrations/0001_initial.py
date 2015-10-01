# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('url', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LinksTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.TextField()),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translation', editable=False, to='popit.Links', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'popit_links_translation',
                'db_tablespace': '',
            },
        ),
        migrations.AlterUniqueTogether(
            name='linkstranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
