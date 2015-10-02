__author__ = 'sweemeng'
from django.db import models
from hvad.models import TranslatableModel
from hvad.models import TranslatedFields
from django.utils.translation import ugettext_lazy as _



# TODO: Override save
# TODO: Citation table is outside of model. Why? Multiple source of information
# TODO: Ensure each field have a citation,
# TODO: Do not save if citation do not exist
class Person(TranslatableModel):
    id = models.CharField(max_length=255, primary_key=True)
    translations = TranslatedFields(
        name = models.CharField(max_length=255, verbose_name=_("name")),
        family_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("family name")),
        given_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("given name")),
        additional_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("additional name")),
        # Because not everyone is a Datuk or Datin
        honorific_prefix = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("honorific prefix")),
        # Usually when Malaysian are Datuk, there is nothing in the end
        honorific_suffix = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("honorific suffix")),
        patronymic_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("patronymic name")), # What the heck is that!
        sort_name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("sort name")), # What on earth....
        gender = models.CharField(max_length=25, null=True, blank=True, verbose_name=_("gender")),
        summary = models.CharField(max_length=255, blank=True, verbose_name=_("summary")), # Member of the human race
        biography = models.TextField(blank=True, verbose_name=_("biography")),
        # Actually should should validate this? Easier if we don't though
        # Also dual citizenship
        national_identity = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("national identify")),

    )

    email = models.EmailField(null=True, verbose_name=_("email")) # Because we happen to have a lot of unusable email.

    birth_date = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("birth date"))
    death_date = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("death data"))
    image = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("image links")) # Maybe I should have a default image path :-/

    created_at = models.DateField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateField(auto_now=True, verbose_name=_("Updated at"))

    def citation_exist(self, field):
        pass