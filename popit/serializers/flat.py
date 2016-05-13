from popit.models import Post
from popit.models import Person
from popit.models import Organization
from rest_framework.serializers import CharField
from hvad.contrib.restframework import TranslatableModelSerializer


class PostFlatSerializer(TranslatableModelSerializer):
    id = CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    organization_id = CharField(max_length=255, required=False)
    area_id = CharField(max_length=255, required=False)

    start_date = CharField(allow_null=True, default=None, allow_blank=True)
    end_date = CharField(allow_null=True, default=None, allow_blank=True)

    class Meta:
        model = Post
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class PersonFlatSerializer(TranslatableModelSerializer):
    id = CharField(max_length=255, required=False, allow_null=True, allow_blank=True)

    birth_date = CharField(allow_null=True, default=None, allow_blank=True)
    death_date = CharField(allow_null=True, default=None, allow_blank=True)

    class Meta:
        model = Person
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class OrganizationFlatSerializer(TranslatableModelSerializer):
    id = CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    parent_id = CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    area_id = CharField(max_length=255, required=False)
    founding_date = CharField(allow_null=True, default=None, allow_blank=True)
    dissolution_date = CharField(allow_null=True, default=None, required=False, allow_blank=True)

    class Meta:
        model = Organization
        extra_kwargs = {'id': {'read_only': False, 'required': False}}