__author__ = 'sweemeng'
from django.db import models
from hvad.models import TranslatableModel
from hvad.models import TranslatedFields
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from popit.models.misc import OtherName
from popit.models.misc import Contact
from popit.models.misc import Link
from popit.models.misc import Identifier
from popit.models.exception import PopItFieldNotExist
import uuid


# Citation table is outside of model. Why? Multiple source of information
class Person(TranslatableModel):
    id = models.CharField(max_length=255, primary_key=True, blank=True)
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

    other_names = GenericRelation(OtherName)
    links = GenericRelation(Link)
    identifiers = GenericRelation(Identifier)
    contacts = GenericRelation(Contact)

    created_at = models.DateField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateField(auto_now=True, verbose_name=_("Updated at"))

    def add_citation(self, field, url, note):
        if not hasattr(self, field):
            raise PopItFieldNotExist("%s Does not exist" % field)
        link = Link.objects.language(self.language_code).create(
            field = field,
            url = url,
            note = note,
            content_object=self
        )

    def citation_exist(self, field):
        if not hasattr(self, field):
            raise PopItFieldNotExist("%s Does not exist" % field)
        links = self.links.language(self.language_code).filter(field=field)
        if links:
            return True
        return False

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        super(Person, self).save(*args, **kwargs)


