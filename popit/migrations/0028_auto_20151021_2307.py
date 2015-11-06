# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0027_auto_20151021_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='area',
            field=models.ForeignKey(to='popit.Area', null=True),
        ),
    ]
