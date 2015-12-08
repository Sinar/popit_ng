# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0043_auto_20151114_1425'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='end_date',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='end date', validators=[django.core.validators.RegexValidator(b'^[0-9]{4}(-[0-9]{2}){0,2}$')]),
        ),
        migrations.AlterField(
            model_name='membership',
            name='start_date',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='start date', validators=[django.core.validators.RegexValidator(b'^[0-9]{4}(-[0-9]{2}){0,2}$')]),
        ),
        migrations.AlterField(
            model_name='organization',
            name='dissolution_date',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='dissolution date', validators=[django.core.validators.RegexValidator(b'^[0-9]{4}(-[0-9]{2}){0,2}$')]),
        ),
        migrations.AlterField(
            model_name='organization',
            name='founding_date',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='founding date', validators=[django.core.validators.RegexValidator(b'^[0-9]{4}(-[0-9]{2}){0,2}$')]),
        ),
        migrations.AlterField(
            model_name='othername',
            name='end_date',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(b'^[0-9]{4}(-[0-9]{2}){0,2}$')]),
        ),
        migrations.AlterField(
            model_name='othername',
            name='start_date',
            field=models.CharField(blank=True, max_length=20, null=True, validators=[django.core.validators.RegexValidator(b'^[0-9]{4}(-[0-9]{2}){0,2}$')]),
        ),
        migrations.AlterField(
            model_name='person',
            name='birth_date',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='birth date', validators=[django.core.validators.RegexValidator(b'^[0-9]{4}(-[0-9]{2}){0,2}$')]),
        ),
        migrations.AlterField(
            model_name='person',
            name='death_date',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='death data', validators=[django.core.validators.RegexValidator(b'^[0-9]{4}(-[0-9]{2}){0,2}$')]),
        ),
        migrations.AlterField(
            model_name='post',
            name='end_date',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='end date', validators=[django.core.validators.RegexValidator(b'^[0-9]{4}(-[0-9]{2}){0,2}$')]),
        ),
        migrations.AlterField(
            model_name='post',
            name='start_date',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='start date', validators=[django.core.validators.RegexValidator(b'^[0-9]{4}(-[0-9]{2}){0,2}$')]),
        ),
    ]
