# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0041_auto_20151113_0120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membershiptranslation',
            name='label',
            field=models.CharField(max_length=255, null=True, verbose_name='Label', blank=True),
        ),
    ]
