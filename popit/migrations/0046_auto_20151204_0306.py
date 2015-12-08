# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0045_auto_20151204_0241'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactdetail',
            name='valid_from',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='valid from', validators=[django.core.validators.RegexValidator(b'^[0-9]{4}(-[0-9]{2}){0,2}$')]),
        ),
        migrations.AlterField(
            model_name='contactdetail',
            name='valid_until',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='valid until', validators=[django.core.validators.RegexValidator(b'^[0-9]{4}(-[0-9]{2}){0,2}$')]),
        ),
    ]
