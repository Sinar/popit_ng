# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0038_auto_20151106_0445'),
    ]

    operations = [
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True, blank=True)),
                ('start_date', models.CharField(max_length=20, null=True, verbose_name='start date', blank=True)),
                ('end_date', models.CharField(max_length=20, null=True, verbose_name='end date', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('area', models.ForeignKey(verbose_name='area', blank=True, to='popit.Area', null=True)),
                ('on_behalf_of', models.ForeignKey(related_name='on_behalf_of', verbose_name='on_behalf_of', blank=True, to='popit.Organization', null=True)),
                ('organization', models.ForeignKey(verbose_name='organization', blank=True, to='popit.Organization', null=True)),
                ('person', models.ForeignKey(verbose_name='person', blank=True, to='popit.Person', null=True)),
                ('post', models.ForeignKey(verbose_name='post', blank=True, to='popit.Post', null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MembershipTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=255, verbose_name='Label')),
                ('role', models.CharField(max_length=255, null=True, verbose_name='role', blank=True)),
                ('language_code', models.CharField(max_length=15, db_index=True)),
                ('master', models.ForeignKey(related_name='translated', editable=False, to='popit.Membership', null=True)),
            ],
            options={
                'managed': True,
                'abstract': False,
                'db_table': 'popit_membership_translation',
                'db_tablespace': '',
            },
        ),
        migrations.AlterUniqueTogether(
            name='membershiptranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
