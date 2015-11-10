# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('popit', '0037_auto_20151106_0319'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactDetail',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True, blank=True)),
                ('type', models.CharField(max_length=255, verbose_name='type')),
                ('value', models.CharField(max_length=255, verbose_name='value')),
                ('valid_from', models.DateField(null=True, verbose_name='valid from', blank=True)),
                ('valid_until', models.DateField(null=True, verbose_name='valid until', blank=True)),
                ('object_id', models.CharField(max_length=255)),
                ('created_at', models.DateField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateField(auto_now=True, verbose_name='updated at')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactDetailTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255, null=True, verbose_name='label', blank=True)),
                ('note', models.TextField(null=True, verbose_name='note', blank=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translation', editable=False, to='popit.ContactDetail', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'popit_contactdetail_translation',
                'db_tablespace': '',
            },
        ),
        migrations.AlterUniqueTogether(
            name='contactdetailtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
