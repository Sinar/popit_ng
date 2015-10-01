# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='links',
            name='label',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
