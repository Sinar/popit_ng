# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('popit', '0016_auto_20151001_0131'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('type', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('valid_from', models.DateField(null=True)),
                ('valid_until', models.DateField(null=True)),
                ('object_id', models.CharField(max_length=255)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Identifier',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('identifier', models.CharField(max_length=255)),
                ('object_id', models.CharField(max_length=255)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('label', models.CharField(max_length=255, null=True)),
                ('field', models.CharField(max_length=20, null=True)),
                ('url', models.URLField()),
                ('object_id', models.CharField(max_length=255)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OtherName',
            fields=[
                ('id', models.CharField(max_length=255, serialize=False, primary_key=True)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('object_id', models.CharField(max_length=255)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('note', models.TextField(null=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RenameModel(
            old_name='ContactsTranslation',
            new_name='ContactTranslation',
        ),
        migrations.RenameModel(
            old_name='IdentifiersTranslation',
            new_name='IdentifierTranslation',
        ),
        migrations.RenameModel(
            old_name='LinksTranslation',
            new_name='LinkTranslation',
        ),
        migrations.RenameModel(
            old_name='OtherNamesTranslation',
            new_name='OtherNameTranslation',
        ),
        migrations.RenameModel(
            old_name='Persons',
            new_name='Person',
        ),
        migrations.RenameModel(
            old_name='PersonsTranslation',
            new_name='PersonTranslation',
        ),
        migrations.RemoveField(
            model_name='contacts',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='identifiers',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='links',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='othernames',
            name='content_type',
        ),
        migrations.AlterField(
            model_name='contacttranslation',
            name='master',
            field=models.ForeignKey(related_name='translation', editable=False, to='popit.Contact', null=True),
        ),
        migrations.AlterField(
            model_name='identifiertranslation',
            name='master',
            field=models.ForeignKey(related_name='translations', editable=False, to='popit.Identifier', null=True),
        ),
        migrations.AlterField(
            model_name='linktranslation',
            name='master',
            field=models.ForeignKey(related_name='translation', editable=False, to='popit.Link', null=True),
        ),
        migrations.AlterField(
            model_name='othernametranslation',
            name='master',
            field=models.ForeignKey(related_name='translations', editable=False, to='popit.OtherName', null=True),
        ),
        migrations.AlterModelTable(
            name='contacttranslation',
            table='popit_contact_translation',
        ),
        migrations.AlterModelTable(
            name='identifiertranslation',
            table='popit_identifier_translation',
        ),
        migrations.AlterModelTable(
            name='linktranslation',
            table='popit_link_translation',
        ),
        migrations.AlterModelTable(
            name='othernametranslation',
            table='popit_othername_translation',
        ),
        migrations.AlterModelTable(
            name='persontranslation',
            table='popit_person_translation',
        ),
        migrations.DeleteModel(
            name='Contacts',
        ),
        migrations.DeleteModel(
            name='Identifiers',
        ),
        migrations.DeleteModel(
            name='Links',
        ),
        migrations.DeleteModel(
            name='OtherNames',
        ),
    ]
