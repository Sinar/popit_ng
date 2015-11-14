# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0039_auto_20151112_0054'),
    ]

    operations = [
        migrations.AddField(
            model_name='membership',
            name='member',
            field=models.ForeignKey(related_name='member', verbose_name='member', blank=True, to='popit.Organization', null=True),
        ),
    ]
