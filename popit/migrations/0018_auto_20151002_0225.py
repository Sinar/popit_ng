# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0017_auto_20151002_0204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='valid_from',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='valid_until',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='field',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='label',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='othername',
            name='end_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='othername',
            name='note',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='othername',
            name='start_date',
            field=models.DateField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='othernametranslation',
            name='additional_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='othernametranslation',
            name='family_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='othernametranslation',
            name='given_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='othernametranslation',
            name='honor_prefix',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='othernametranslation',
            name='honor_suffix',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='othernametranslation',
            name='patronymic_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='birth_date',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='death_date',
            field=models.CharField(max_length=20, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='additional_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='biography',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='family_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='gender',
            field=models.CharField(max_length=25, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='given_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='honorific_prefix',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='honorific_suffix',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='national_identity',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='patronymic_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='sort_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
