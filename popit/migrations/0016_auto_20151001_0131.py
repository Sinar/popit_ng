# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0015_auto_20151001_0130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contacts',
            name='valid_from',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='valid_until',
            field=models.DateField(null=True),
        ),
    ]
