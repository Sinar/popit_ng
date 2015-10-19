# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0024_auto_20151019_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 1, 45, 19, 747565), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='area',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 10, 19, 1, 45, 26, 392687), auto_now=True),
            preserve_default=False,
        ),
    ]
