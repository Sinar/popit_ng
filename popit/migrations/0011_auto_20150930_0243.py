# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('popit', '0010_links_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='links',
            name='content_type',
            field=models.ForeignKey(default='', to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='links',
            name='object_id',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
