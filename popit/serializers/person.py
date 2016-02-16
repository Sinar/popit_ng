__author__ = 'sweemeng'
from popit.models import Person
from popit.models import ContactDetail
from popit.models import Link
from popit.models import Identifier
from popit.models import OtherName
from popit.models import Membership
from hvad.contrib.restframework import TranslatableModelSerializer
from rest_framework.serializers import CharField
from popit.serializers.misc import OtherNameSerializer
from popit.serializers.misc import IdentifierSerializer
from popit.serializers.misc import LinkSerializer
from popit.serializers.misc import ContactDetailSerializer
from popit.serializers.misc import AreaSerializer
from rest_framework.serializers import ValidationError
import re


class PersonMembershipSerializer(TranslatableModelSerializer):

    id = CharField(max_length=255, required=False)
    person_id = CharField(max_length=255, required=False)
    organization_id = CharField(max_length=255, required=False)
    member_id = CharField(max_length=255, required=False)
    on_behalf_of_id = CharField(max_length=255, required=False)
    area_id = CharField(max_length=255, required=False, allow_null=True)
    post_id = CharField(max_length=255, required=False, allow_null=True)

    contact_details = ContactDetailSerializer(many=True, required=False)
    links = LinkSerializer(many=True, required=False)
    start_date = CharField(allow_null=True, default=None, allow_blank=True)
    end_date = CharField(allow_null=True, default=None, allow_blank=True)

    class Meta:
        model = Membership
        extra_kwargs = {'id': {'read_only': False, 'required': False}}
        exclude = ["person", "organization", "post", "area"]


class PersonSerializer(TranslatableModelSerializer):

    id = CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    other_names = OtherNameSerializer(many=True, required=False)
    identifiers = IdentifierSerializer(many=True, required=False)
    memberships = PersonMembershipSerializer(many=True, required=False)
    links = LinkSerializer(many=True, required=False)
    contact_details = ContactDetailSerializer(many=True, required=False)
    birth_date = CharField(allow_null=True, default=None, allow_blank=True)
    death_date = CharField(allow_null=True, default=None, allow_blank=True)

    def create(self, validated_data):
        language_code=self.language
        links = validated_data.pop("links", [])
        other_names = validated_data.pop("other_names", [])
        contact_details = validated_data.pop('contact_details', [])
        identifiers = validated_data.pop("identifiers", [])
        # Where do the language come from inside the create function
        validated_data.pop("language_code", [])
        validated_data.pop("memberships", None)
        # So that elasticsearch handle this sanely
        if not validated_data["birth_date"]:
            validated_data["birth_date"] = None
        if not validated_data["death_date"]:
            validated_data["death_date"] = None

        person = Person.objects.language(language_code).create(**validated_data)

        for other_name in other_names:
            self.create_child(other_name, OtherName, person)

        for contact in contact_details:
            self.create_child(contact, ContactDetail, person)

        for identifier in identifiers:
            self.create_child(identifier, Identifier, person)

        for link in links:
            self.create_links(link, person)
        return person

    def create_links(self, validated_data, entity):
        language_code = self.language
        validated_data["content_object"] = entity
        Link.objects.language(language_code).create(**validated_data)

    def create_child(self, validated_data, child, parent):
        links = validated_data.pop("links", [])
        language_code = self.language
        validated_data["content_object"] = parent
        obj = child.objects.language(language_code).create(**validated_data)
        for link in links:
            self.create_links(link, obj)

    # The reason why allow creation of related item is, each field is not stand alone, it require a parent item.
    # The possible exception is membership in popolo, but it is not implemented yet
    def update(self, instance, validated_data):
        """

        :param instance:
        :param validated_data:
        :return:
        """
        available_language = instance.get_available_languages()
        if not self.language in available_language:
            instance = instance.translate(self.language)
        # Now sure if save everytime we update a good idea. On the other hand, not like everyone can update anyway.
        # Also some field is not added, maybe I should add patronymic name and sort name =.=
        instance.name = validated_data.get("name", instance.name)
        instance.family_name = validated_data.get("family_name", instance.name)
        instance.given_name = validated_data.get("given_name", instance.given_name)
        instance.additional_name = validated_data.get("additional_name", instance.additional_name)
        instance.honorific_prefix = validated_data.get("honorific_prefix", instance.honorific_prefix)
        instance.honorific_suffix = validated_data.get("honorific_suffix", instance.honorific_suffix)
        instance.email = validated_data.get("email", instance.email)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.birth_date = validated_data.get("birth_date", instance.birth_date)
        # Keep elasticseach sane
        if not instance.birth_date:
            instance.birth_date = None
        instance.death_date = validated_data.get("death_date", instance.death_date)
        if not instance.death_date:
            instance.death_date = None
        instance.image = validated_data.get("image", instance.image)
        instance.summary = validated_data.get("summary", instance.summary)
        instance.biography = validated_data.get("biography", instance.biography)
        instance.national_identity = validated_data.get("national_identity", instance.national_identity)
        instance.save()

        links = validated_data.pop("links", [])
        for link in links:
            self.update_links(link, instance)

        identifiers = validated_data.pop("identifiers", [])

        for identifier in identifiers:
            self.update_childs(identifier, Identifier, instance)

        contact_details = validated_data.pop("contact_details", [])
        for contact in contact_details:
            self.update_childs(contact, ContactDetail, instance)

        other_names = validated_data.pop("other_names", [])
        for other_name in other_names:
            self.update_childs(other_name, OtherName, instance)
        return instance

    def update_childs(self, validated_data, child, parent):
        # parent mostly exist at create,
        language_code = parent.language_code
        if validated_data.get("id"):
            objs = child.objects.language(language_code).filter(id=validated_data.get("id"))
            if not objs:
                self.create_child(validated_data, child, parent)
            else:
                obj = objs[0]

                links = validated_data.pop("links", [])

                for key, value in validated_data.iteritems():
                    if key in ("id", "language_code", "created_at" "updated_at"):
                        continue
                    setattr(obj, key, value)

                obj.save()

                for link in links:
                    self.update_links(link, obj)
        else:
            self.create_child(validated_data, child, parent)

    def update_links(self, validated_data, parent):
        language_code = parent.language_code

        if validated_data.get("id"):
            links = Link.objects.language(language_code).filter(id=validated_data.get("id"))
            if not links:
                self.create_links(validated_data, parent)
            else:
                link = links[0]
                link.label = validated_data.get("label", link.label)
                link.field = validated_data.get("field", link.field)
                link.url = validated_data.get("url", link.url)
                link.note = validated_data.get("note", link.note)
                link.save()
        else:
            self.create_links(validated_data, parent)

    def to_representation(self, instance):
        data = super(PersonSerializer, self).to_representation(instance)
        # Now we do all the overriding

        other_name_instance = instance.other_names.untranslated().all()
        other_name_serializer = OtherNameSerializer(instance=other_name_instance, many=True, language=instance.language_code)
        data["other_names"] = other_name_serializer.data

        identifier_instance = instance.identifiers.untranslated().all()
        identifier_serializer = IdentifierSerializer(instance=identifier_instance, many=True, language=instance.language_code)
        data["identifiers"] = identifier_serializer.data

        links_instance = instance.links.untranslated().all()
        links_serializer = LinkSerializer(instance=links_instance, many=True, language=instance.language_code)
        data["links"] = links_serializer.data

        contact_details_instance = instance.contact_details.untranslated().all()
        contact_details_serializer = ContactDetailSerializer(instance=contact_details_instance, many=True,
                                                             language=instance.language_code)
        data["contact_details"] = contact_details_serializer.data

        return data

    def validate_birth_date(self, value):
        if not value:
            return value
        if not re.match(r"^[0-9]{4}(-[0-9]{2}){0,2}$", value):
            raise ValidationError("value need to be in in ^[0-9]{4}(-[0-9]{2}){0,2}$ format")
        return value

    def validate_death_date(self, value):
        if not value:
            return None
        if not re.match(r"^[0-9]{4}(-[0-9]{2}){0,2}$", value):
            raise ValidationError("value need to be in in ^[0-9]{4}(-[0-9]{2}){0,2}$ format")
        return value

    class Meta:
        model = Person
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


