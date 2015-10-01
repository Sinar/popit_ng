# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0014_auto_20150930_0421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='othernames',
            name='note',
            field=models.TextField(null=True),
        ),
    ]
