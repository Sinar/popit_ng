# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0019_auto_20151002_0248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='othernametranslation',
            name='honor_prefix',
        ),
        migrations.RemoveField(
            model_name='othernametranslation',
            name='honor_suffix',
        ),
        migrations.AddField(
            model_name='othernametranslation',
            name='honorific_prefix',
            field=models.CharField(max_length=255, null=True, verbose_name='honorific prefix', blank=True),
        ),
        migrations.AddField(
            model_name='othernametranslation',
            name='honorific_suffix',
            field=models.CharField(max_length=255, null=True, verbose_name='honorific suffix', blank=True),
        ),
    ]
