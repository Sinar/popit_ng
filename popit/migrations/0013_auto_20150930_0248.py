# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0012_auto_20150930_0247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='identifiers',
            name='sources',
        ),
        migrations.RemoveField(
            model_name='othernames',
            name='end_date_source',
        ),
        migrations.RemoveField(
            model_name='othernames',
            name='start_date_source',
        ),
        migrations.RemoveField(
            model_name='othernamestranslation',
            name='add_name_source',
        ),
        migrations.RemoveField(
            model_name='othernamestranslation',
            name='family_name_source',
        ),
        migrations.RemoveField(
            model_name='othernamestranslation',
            name='given_name_source',
        ),
        migrations.RemoveField(
            model_name='othernamestranslation',
            name='honor_prefix_source',
        ),
        migrations.RemoveField(
            model_name='othernamestranslation',
            name='honor_suffix_source',
        ),
        migrations.RemoveField(
            model_name='othernamestranslation',
            name='name_source',
        ),
        migrations.RemoveField(
            model_name='othernamestranslation',
            name='patron_name_source',
        ),
    ]
