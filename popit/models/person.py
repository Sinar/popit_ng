__author__ = 'sweemeng'
from django.db import models
from hvad.models import TranslatableModel
from hvad.models import TranslatedFields



# TODO: Override save
# TODO: Citation table is outside of model. Why? Multiple source of information
# TODO: Ensure each field have a citation,
# TODO: Do not save if citation do not exist
class Persons(TranslatableModel):
    id = models.CharField(max_length=255, primary_key=True)
    translations = TranslatedFields(
        name = models.CharField(max_length=255),
        family_name = models.CharField(max_length=255, null=True),
        given_name = models.CharField(max_length=255, null=True),
        additional_name = models.CharField(max_length=255, null=True),
        honorific_prefix = models.CharField(max_length=255, null=True), # Because not everyone is a Datuk or Datin
        honorific_suffix = models.CharField(max_length=255, null=True), # Usually when Malaysian are Datuk, there is nothing in the end
        patronymic_name = models.CharField(max_length=255, null=True), # What the heck is that!
        sort_name = models.CharField(max_length=255, null=True), # What on earth....
        gender = models.CharField(max_length=25, null=True),
        summary = models.CharField(max_length=255, blank=True), # Member of the human race
        biography = models.TextField(),
        national_identity = models.CharField(max_length=255), # Actually should should validate this? Easier if we don't though
        # Also dual citizenship
    )

    email = models.EmailField(null=True) # Because we happen to have a lot of unusable email.

    birth_date = models.CharField(max_length=20, null=True)
    death_date = models.CharField(max_length=20, null=True)
    image = models.CharField(max_length=255, null=True) # Maybe I should have a default image path :-/

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def citation_exist(self, field):
        pass