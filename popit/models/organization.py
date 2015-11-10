__author__ = 'sweemeng'
from django.db import models
from hvad.models import TranslatableModel
from hvad.models import TranslatedFields
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from popit.models.misc import OtherName
from popit.models.misc import Contact
from popit.models.misc import ContactDetail
from popit.models.misc import Link
from popit.models.misc import Identifier
from popit.models.misc import Area
from popit.models.exception import PopItFieldNotExist
import uuid


class Organization(TranslatableModel):
    id = models.CharField(max_length=255, primary_key=True, blank=True)
    translated = TranslatedFields(
        name = models.CharField(max_length=255, verbose_name=_('name')),
        classification = models.CharField(max_length=255, verbose_name=_('classification'), null=True, blank=True),
        abstract = models.CharField(max_length=255, verbose_name=_('abstract'), null=True, blank=True),
        description = models.TextField(verbose_name=_('description'), null=True, blank=True)
    )

    parent = models.ForeignKey('self', related_name='children', null=True, blank=True)

    area = models.ForeignKey(Area, null=True, blank=True)
    founding_date = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('founding date'))
    dissolution_date = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('dissolution date'))

    image = models.URLField(null=True, blank=True, verbose_name=_('image'))

    other_names = GenericRelation(OtherName)
    contact_details = GenericRelation(ContactDetail)
    identifiers = GenericRelation(Identifier)
    links = GenericRelation(Link)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('updated at'))

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
        super(Organization, self).save(*args, **kwargs)

    def __unicode__(self):
        # Why is it that they do not find name, but need self.name
        # Actually what could go wrong if we switch to bm
        return self.safe_translation_getter('name', self.name)

