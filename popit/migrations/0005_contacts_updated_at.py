# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0004_auto_20150928_0509'),
    ]

    operations = [
        migrations.AddField(
            model_name='contacts',
            name='updated_at',
            field=models.DateField(default=datetime.date(2015, 9, 28), auto_now=True),
            preserve_default=False,
        ),
    ]
