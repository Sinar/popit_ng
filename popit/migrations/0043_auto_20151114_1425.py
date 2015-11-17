# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0042_auto_20151113_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='organization',
            field=models.ForeignKey(related_name='membership', verbose_name='organization', blank=True, to='popit.Organization', null=True),
        ),
    ]
