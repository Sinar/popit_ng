# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0021_auto_20151005_0250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='id',
            field=models.CharField(max_length=255, serialize=False, primary_key=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contacttranslation',
            name='label',
            field=models.CharField(max_length=255, null=True, verbose_name='label', blank=True),
        ),
        migrations.AlterField(
            model_name='contacttranslation',
            name='note',
            field=models.TextField(null=True, verbose_name='note', blank=True),
        ),
        migrations.AlterField(
            model_name='identifier',
            name='id',
            field=models.CharField(max_length=255, serialize=False, primary_key=True, blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='id',
            field=models.CharField(max_length=255, serialize=False, primary_key=True, blank=True),
        ),
        migrations.AlterField(
            model_name='linktranslation',
            name='note',
            field=models.TextField(null=True, verbose_name='note', blank=True),
        ),
        migrations.AlterField(
            model_name='othername',
            name='id',
            field=models.CharField(max_length=255, serialize=False, primary_key=True, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='id',
            field=models.CharField(max_length=255, serialize=False, primary_key=True, blank=True),
        ),
    ]
