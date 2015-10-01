__author__ = 'sweemeng'
from django.db import models
from hvad.models import TranslatableModel
from hvad.models import TranslatedFields
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# Yay Popolo+!

# This is the source,
class Links(TranslatableModel):
    id = models.CharField(max_length=255, primary_key=True)
    label = models.CharField(max_length=255, null=True)
    field = models.CharField(max_length=20, null=True) # This is our plus stuff, for citation
    url = models.URLField()
    translation = TranslatedFields(
        note = models.TextField()
    )
    object_id = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Contacts(TranslatableModel):
    id = models.CharField(max_length=255, primary_key=True)
    translation = TranslatedFields(
        label = models.CharField(max_length=255), # hopefully people won't be searching via label :-/
        note = models.TextField()
    )
    type = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    valid_from = models.DateField(null=True)
    valid_until = models.DateField(null=True)
    object_id = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Identifiers(TranslatableModel):
    id = models.CharField(max_length=255, primary_key=True)
    identifier = models.CharField(max_length=255)
    translations = TranslatedFields(
        scheme = models.CharField(max_length=255)
    )

    object_id = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey("content_type", "object_id")

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


# In media, only translated name is used not name in original language
# unless name uses a different character than in original language :-/
# Name and other thing need sources
# Usecase, Name is on wiki, nick name might be on newspaper, (who actually have that)
# TODO: Find convenience method
# You know, this is made simple if we use a json field, hvad might choked on it though
class OtherNames(TranslatableModel):
    id = models.CharField(max_length=255, primary_key=True)
    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        family_name = models.CharField(max_length=255, null=True), # We don't always get the name of the fllowing field
        given_name = models.CharField(max_length=255, null=True),
        additional_name = models.CharField(max_length=255, null=True),
        honor_prefix = models.CharField(max_length=255, null=True), # Not everyone a datuk/datin/etc
        honor_suffix = models.CharField(max_length=255, null=True), # Datuk someone, and that's it.
        patronymic_name = models.CharField(max_length=255, null=True),
    )
    start_date = models.DateField(null=True) # Sometime we have no idea
    end_date = models.DateField(null=True)

    object_id = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey("content_type", "object_id")

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    note = models.TextField(null=True)
