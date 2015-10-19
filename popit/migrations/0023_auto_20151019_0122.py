# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0022_auto_20151009_0155'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True, blank=True)),
                ('identifier', models.CharField(max_length=255, null=True, verbose_name='identifier', blank=True)),
                ('parent', models.ForeignKey(related_name='children', to='popit.Area')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AreaTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('classification', models.CharField(max_length=20, null=True, verbose_name='classification', blank=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='popit.Area', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'popit_area_translation',
                'db_tablespace': '',
            },
        ),
        migrations.AlterUniqueTogether(
            name='areatranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
