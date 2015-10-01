# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0002_links_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='links',
            name='created_at',
            field=models.DateField(default=datetime.date(2015, 9, 28), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='links',
            name='updated_at',
            field=models.DateField(default=datetime.date(2015, 9, 28), auto_now=True),
            preserve_default=False,
        ),
    ]
