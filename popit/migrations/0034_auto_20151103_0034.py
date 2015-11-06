# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0033_auto_20151030_0640'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='area',
            field=models.ForeignKey(blank=True, to='popit.Area', null=True),
        ),
    ]
