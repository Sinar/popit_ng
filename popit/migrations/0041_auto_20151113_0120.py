# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('popit', '0040_membership_member'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='person',
            field=models.ForeignKey(default=2, verbose_name='person', to='popit.Person'),
            preserve_default=False,
        ),
    ]
