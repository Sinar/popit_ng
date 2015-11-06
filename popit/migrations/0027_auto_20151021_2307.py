# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0026_auto_20151019_0250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='parent',
            field=models.ForeignKey(related_name='children', to='popit.Organization', null=True),
        ),
    ]
