# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-03-07 01:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0053_auto_20160201_0236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='areatranslation',
            name='classification',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='classification'),
        ),
    ]