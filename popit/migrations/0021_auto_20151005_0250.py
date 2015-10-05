# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0020_auto_20151002_0249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='othername',
            name='end_date',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='othername',
            name='start_date',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
    ]
