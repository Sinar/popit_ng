# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0003_auto_20150928_0156'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('valid_from', models.DateField()),
                ('valid_until', models.DateField()),
                ('created_at', models.DateField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactsTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255)),
                ('note', models.TextField()),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translation', editable=False, to='popit.Contacts', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'popit_contacts_translation',
                'db_tablespace': '',
            },
        ),
        migrations.AlterUniqueTogether(
            name='contactstranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
