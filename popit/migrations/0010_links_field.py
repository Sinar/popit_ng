# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0009_auto_20150930_0223'),
    ]

    operations = [
        migrations.AddField(
            model_name='links',
            name='field',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
