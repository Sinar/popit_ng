# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0034_auto_20151103_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posttranslation',
            name='label',
            field=models.CharField(max_length=255, null=True, verbose_name='label', blank=True),
        ),
    ]
