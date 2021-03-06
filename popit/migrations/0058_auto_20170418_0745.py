# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2017-04-18 07:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0057_auto_20170315_0222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relation',
            name='object',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations_as_object', to='popit.Person', verbose_name='object'),
        ),
        migrations.AlterField(
            model_name='relation',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relations_as_subject', to='popit.Person', verbose_name='subject'),
        ),
    ]
