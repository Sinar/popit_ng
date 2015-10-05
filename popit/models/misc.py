__author__ = 'sweemeng'
from django.db import models
from hvad.models import TranslatableModel
from hvad.models import TranslatedFields
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import ugettext_lazy as _


# Yay Popolo+!

# This is the source,
class Link(TranslatableModel):
    id = models.CharField(max_length=255, primary_key=True)
    label = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("label"))
    # This is our plus stuff, for citation
    field = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("field"))
    url = models.URLField(verbose_name=_("url"))
    translation = TranslatedFields(
        note = models.TextField(verbose_name=_("note"))
    )
    object_id = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateField(auto_now=True, verbose_name=_("updated at"))


class Contact(TranslatableModel):
    id = models.CharField(max_length=255, primary_key=True)
    translation = TranslatedFields(
        label = models.CharField(max_length=255, verbose_name=_("label")), # hopefully people won't be searching via label :-/
        note = models.TextField(verbose_name=_("note"))
    )
    type = models.CharField(max_length=255, verbose_name=_("type"))
    value = models.CharField(max_length=255, verbose_name=_("value"))
    valid_from = models.DateField(null=True, blank=True, verbose_name=_("valid from"))
    valid_until = models.DateField(null=True, blank=True, verbose_name=_("valid until"))
    object_id = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey("content_type", "object_id")
    created_at = models.DateField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateField(auto_now=True, verbose_name=_("updated at"))


class Identifier(TranslatableModel):
    id = models.CharField(max_length=255, primary_key=True)
    identifier = models.CharField(max_length=255, verbose_name=_("identifier"))
    translations = TranslatedFields(
        scheme = models.CharField(max_length=255, verbose_name=_("scheme")) # This is not actually skim in Malay fyi
    )

    object_id = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey("content_type", "object_id")

    created_at = models.DateField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateField(auto_now=True, verbose_name=_("updated at"))


# In media, only translated name is used not name in original language
# unless name uses a different character than in original language :-/
# Name and other thing need sources
# Usecase, Name is on wiki, nick name might be on newspaper, (who actually have that)
# TODO: Find convenience method
# You know, this is made simple if we use a json field, hvad might choked on it though
class OtherName(TranslatableModel):
    id = models.CharField(max_length=255, primary_key=True)
    translations = TranslatedFields(
        name = models.CharField(max_length=255, verbose_name=_("name")),
         # We don't always get the name of the fllowing field
        family_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("family name")),
        given_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("given name")),
        additional_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("additional name")),
        # Not everyone a datuk/datin/etc
        honorific_prefix = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("honorific prefix")),
        # Datuk someone, and that's it.
        honorific_suffix = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("honorific suffix")),
        patronymic_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("patronymmic name")),
    )
    start_date = models.CharField(max_length=20, null=True, blank=True) # Sometime we have no idea
    end_date = models.CharField(max_length=20, null=True, blank=True)

    object_id = models.CharField(max_length=255)
    content_type = models.ForeignKey(ContentType)
    content_object = GenericForeignKey("content_type", "object_id")

    created_at = models.DateField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateField(auto_now=True, verbose_name=_("updated at"))

    note = models.TextField(null=True, blank=True)
