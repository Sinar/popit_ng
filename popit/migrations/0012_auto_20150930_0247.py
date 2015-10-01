# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('popit', '0011_auto_20150930_0243'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacts',
            name='content_type',
            field=models.ForeignKey(default=None, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contacts',
            name='object_id',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='identifiers',
            name='content_type',
            field=models.ForeignKey(default=None, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='identifiers',
            name='object_id',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='othernames',
            name='content_type',
            field=models.ForeignKey(default=None, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='othernames',
            name='object_id',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
