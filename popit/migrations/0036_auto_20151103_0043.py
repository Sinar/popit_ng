# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0035_auto_20151103_0042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posttranslation',
            name='role',
            field=models.CharField(default='member', max_length=20, verbose_name='role'),
            preserve_default=False,
        ),
    ]
