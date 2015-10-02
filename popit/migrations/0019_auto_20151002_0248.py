# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0018_auto_20151002_0225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='type',
            field=models.CharField(max_length=255, verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='valid_from',
            field=models.DateField(null=True, verbose_name='valid from', blank=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='valid_until',
            field=models.DateField(null=True, verbose_name='valid until', blank=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='value',
            field=models.CharField(max_length=255, verbose_name='value'),
        ),
        migrations.AlterField(
            model_name='contacttranslation',
            name='label',
            field=models.CharField(max_length=255, verbose_name='label'),
        ),
        migrations.AlterField(
            model_name='contacttranslation',
            name='note',
            field=models.TextField(verbose_name='note'),
        ),
        migrations.AlterField(
            model_name='identifier',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='identifier',
            name='identifier',
            field=models.CharField(max_length=255, verbose_name='identifier'),
        ),
        migrations.AlterField(
            model_name='identifier',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='identifiertranslation',
            name='scheme',
            field=models.CharField(max_length=255, verbose_name='scheme'),
        ),
        migrations.AlterField(
            model_name='link',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='link',
            name='field',
            field=models.CharField(max_length=20, null=True, verbose_name='field', blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='label',
            field=models.CharField(max_length=255, null=True, verbose_name='label', blank=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='link',
            name='url',
            field=models.URLField(verbose_name='url'),
        ),
        migrations.AlterField(
            model_name='linktranslation',
            name='note',
            field=models.TextField(verbose_name='note'),
        ),
        migrations.AlterField(
            model_name='othername',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='othername',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='othernametranslation',
            name='additional_name',
            field=models.CharField(max_length=255, null=True, verbose_name='additional name', blank=True),
        ),
        migrations.AlterField(
            model_name='othernametranslation',
            name='family_name',
            field=models.CharField(max_length=255, null=True, verbose_name='family name', blank=True),
        ),
        migrations.AlterField(
            model_name='othernametranslation',
            name='given_name',
            field=models.CharField(max_length=255, null=True, verbose_name='given name', blank=True),
        ),
        migrations.AlterField(
            model_name='othernametranslation',
            name='honor_prefix',
            field=models.CharField(max_length=255, null=True, verbose_name='honorary prefix', blank=True),
        ),
        migrations.AlterField(
            model_name='othernametranslation',
            name='honor_suffix',
            field=models.CharField(max_length=255, null=True, verbose_name='honorary suffix', blank=True),
        ),
        migrations.AlterField(
            model_name='othernametranslation',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='othernametranslation',
            name='patronymic_name',
            field=models.CharField(max_length=255, null=True, verbose_name='patronymmic name', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='birth_date',
            field=models.CharField(max_length=20, null=True, verbose_name='birth date', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='person',
            name='death_date',
            field=models.CharField(max_length=20, null=True, verbose_name='death data', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(max_length=254, null=True, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='person',
            name='image',
            field=models.CharField(max_length=255, null=True, verbose_name='image links', blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='updated_at',
            field=models.DateField(auto_now=True, verbose_name='Updated at'),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='additional_name',
            field=models.CharField(max_length=255, null=True, verbose_name='additional name', blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='biography',
            field=models.TextField(verbose_name='biography', blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='family_name',
            field=models.CharField(max_length=255, null=True, verbose_name='family name', blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='gender',
            field=models.CharField(max_length=25, null=True, verbose_name='gender', blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='given_name',
            field=models.CharField(max_length=255, null=True, verbose_name='given name', blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='honorific_prefix',
            field=models.CharField(max_length=255, null=True, verbose_name='honorific prefix', blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='honorific_suffix',
            field=models.CharField(max_length=255, null=True, verbose_name='honorific suffix', blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='name',
            field=models.CharField(max_length=255, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='national_identity',
            field=models.CharField(max_length=255, null=True, verbose_name='national identify', blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='patronymic_name',
            field=models.CharField(max_length=255, null=True, verbose_name='patronymic name', blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='sort_name',
            field=models.CharField(max_length=255, null=True, verbose_name='sort name', blank=True),
        ),
        migrations.AlterField(
            model_name='persontranslation',
            name='summary',
            field=models.CharField(max_length=255, verbose_name='summary', blank=True),
        ),
    ]
