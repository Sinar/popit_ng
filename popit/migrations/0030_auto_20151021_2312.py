# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0029_auto_20151021_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='area',
            field=models.ForeignKey(default=None, blank=True, to='popit.Area'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='organization',
            name='parent',
            field=models.ForeignKey(related_name='children', default=None, blank=True, to='popit.Organization'),
            preserve_default=False,
        ),
    ]
