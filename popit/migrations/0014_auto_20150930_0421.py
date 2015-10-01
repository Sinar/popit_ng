# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0013_auto_20150930_0248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='citation',
            name='content_type',
        ),
        migrations.AlterUniqueTogether(
            name='citationtranslation',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='citationtranslation',
            name='master',
        ),
        migrations.DeleteModel(
            name='Citation',
        ),
        migrations.DeleteModel(
            name='CitationTranslation',
        ),
    ]
