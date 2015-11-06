# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0036_auto_20151103_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posttranslation',
            name='role',
            field=models.CharField(max_length=20, null=True, verbose_name='role', blank=True),
        ),
    ]
