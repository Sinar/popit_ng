# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0031_auto_20151021_2313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='parent',
            field=models.ForeignKey(related_name='children', blank=True, to='popit.Area', null=True),
        ),
    ]
