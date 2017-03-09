from django.db import models
from hvad.models import TranslatableModel
from hvad.models import TranslatedFields
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from popit.models.exception import PopItFieldNotExist
from popit.models import Person
from popit.models import Link
import uuid


class Relation(TranslatableModel):
    id = models.CharField(max_length=255, blank=True, primary_key=True)
    translated = TranslatedFields(
        label = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Label")),
    )

    object = models.ForeignKey(Person, verbose_name=_("object"), related_name="relationships_as_object")
    subject = models.ForeignKey(Person, verbose_name=_("subject"), related_name="relationships_as_subject")
    start_date = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("start date"),
                                  validators=[
                                      RegexValidator("^[0-9]{4}(-[0-9]{2}){0,2}$")
                                  ]
        )
    end_date = models.CharField(max_length=20, null=True, blank=True, verbose_name=_("end date"),
                                validators=[
                                      RegexValidator("^[0-9]{4}(-[0-9]{2}){0,2}$")
                                  ]
                                )
    links = GenericRelation(Link)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("created at"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("updated at"))

    def add_citation(self, field, url, note):
        if not hasattr(self, field):
            raise PopItFieldNotExist("%s Does not exist" % field)
        Link.objects.language(self.language_code).create(
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

        super(Relation, self).save(*args, **kwargs)

    def clean(self):
        super(Relation, self).clean()

    def __unicode__(self):
        return self.safe_translation_getter('label', self.id)
