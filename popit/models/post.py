__author__ = 'sweemeng'
from django.db import models
from hvad.models import TranslatableModel
from hvad.models import TranslatedFields
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import RegexValidator
from popit.models import Organization
from popit.models import Area
from popit.models import OtherName
from popit.models import ContactDetail
from popit.models import Link
from popit.models.exception import PopItFieldNotExist

import uuid


class Post(TranslatableModel):
    id = models.CharField(max_length=255, primary_key=True, blank=True, verbose_name=_("id"))
    translations = TranslatedFields(
        label = models.CharField(max_length=255, verbose_name=_("label"), null=True, blank=True),
        role = models.CharField(max_length=100, verbose_name=_("role"), null=True, blank=True),
    )
    other_labels = GenericRelation(OtherName)
    organization = models.ForeignKey(Organization, null=True, blank=True, related_name="posts")
    area = models.ForeignKey(Area, null=True, blank=True)
    start_date = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("start date"),
                                        validators=[
                                              RegexValidator("^[0-9]{4}(-[0-9]{2}){0,2}$")
                                          ])
    end_date = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("end date"),
                                        validators=[
                                              RegexValidator("^[0-9]{4}(-[0-9]{2}){0,2}$")
                                          ])

    contact_details = GenericRelation(ContactDetail)

    links = GenericRelation(Link)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name=_("updated at"))

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
            id_ = uuid.uuid4()
            self.id = str(id_.hex)
        self.full_clean()
        super(Post, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.organization:
            name = '%s of %s' % (self.safe_translation_getter('role', self.role), self.organization.safe_translation_getter("name", self.organization.id))
        else:
            name = '%s of %s' % (self.safe_translation_getter('role', self.role), "None")
        return name

