__author__ = 'sweemeng'
from popit.models import Person
from popit.models import Contact
from popit.models import ContactDetail
from popit.models import Link
from popit.models import Identifier
from popit.models import OtherName
from hvad.contrib.restframework import TranslatableModelSerializer
from rest_framework.serializers import CharField
from popit.serializers.exceptions import ContentObjectNotAvailable
from popit.models import Area
from rest_framework.serializers import ValidationError
import re


class LinkSerializer(TranslatableModelSerializer):
    id = CharField(max_length=255, required=False)

    def create(self, validated_data):
        language = self.language
        # Really where there language code come from!
        validated_data.pop("language_code", None)
        if not "content_object" in validated_data:
            raise ContentObjectNotAvailable("Please save parent object by callsing serializer.save(content_object=ParentObject)")
        link = Link.objects.language(language).create(**validated_data)
        return link

    def update(self, instance, data):
        instance.label = data.get("label", instance.label)
        instance.field = data.get("field", instance.field)
        instance.url = data.get("url", instance.url)
        instance.note = data.get("note", instance.note)
        instance.save()
        return instance

    class Meta:
        model = Link
        exclude = ('object_id', 'content_type')
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class ContactDetailSerializer(TranslatableModelSerializer):

    id = CharField(max_length=255, required=False)
    links = LinkSerializer(many=True, required=False)

    def create(self, validated_data):
        links = validated_data.pop("links", [])
        # Really where there language code come from!
        validated_data.pop("language_code", None)
        language = self.language
        # content_object must be pass into save parameter
        if not "content_object" in validated_data:
            raise ContentObjectNotAvailable("Please save parent object by callsing serializer.save(content_object=ParentObject)")
        contact = ContactDetail.objects.language(language).create(
            **validated_data
        )
        for link in links:
            self.create_links(link, contact)
        return contact

    def create_links(self, validated_data, entity):
        language_code = self.language
        validated_data["content_object"] = entity
        Link.objects.language(language_code).create(**validated_data)

    def update(self, instance, data):
        links = data.pop("links", [])
        instance.label = data.get("label", instance.label)
        instance.note = data.get('note', instance.note)
        instance.type = data.get('type', instance.type)
        instance.value = data.get('value', instance.value)
        instance.valid_from = data.get('valid_from', instance.valid_from)
        instance.valid_until = data.get('valid_until', instance.valid_until)
        instance.save()
        for link in links:
            self.update_links(link, instance)
        return instance

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
        data = super(ContactDetailSerializer, self).to_representation(instance)

        links_instance = instance.links.untranslated().all()
        links_serializer = LinkSerializer(instance=links_instance, many=True, language=instance.language_code)
        data["links"] = links_serializer.data

        return data

    def validate_valid_from(self, value):
        if not re.match(r"^[0-9]{4}(-[0-9]{2}){0,2}$", value):
            raise ValidationError("value need to be in ^[0-9]{4}(-[0-9]{2}){0,2}$ format")
        return value

    def validate_valid_to(self, value):
        if not re.match(r"^[0-9]{4}(-[0-9]{2}){0,2}$", value):
            raise ValidationError("value need to be in ^[0-9]{4}(-[0-9]{2}){0,2}$ format")
        return value

    class Meta:
        model = ContactDetail
        exclude = ('object_id', 'content_type')
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class IdentifierSerializer(TranslatableModelSerializer):

    id = CharField(max_length=255, required=False)
    links = LinkSerializer(many=True, required=False)

    def create(self, validated_data):
        links = validated_data.pop("links", [])
        # Really where there language code come from!
        validated_data.pop("language_code", None)
        language = self.language
        if not "content_object" in validated_data:
            raise ContentObjectNotAvailable("Please save parent object by calling serializer.save(content_object=ParentObject)")

        identifier = Identifier.objects.language(language).create(**validated_data)
        for link in links:
            self.create_links(link, identifier)

        return identifier

    def create_links(self, validated_data, entity):
        language_code = self.language
        # Really where there language code come from!
        validated_data.pop("language_code", None)
        validated_data["content_object"] = entity
        Link.objects.language(language_code).create(**validated_data)

    def update(self, instance, data):
        links = data.pop('links', [])
        instance.scheme = data.get('scheme', instance.scheme)
        instance.identifier = data.get('identifier', instance.identifier)
        instance.save()
        for link in links:
            self.update_links(link, instance)

        return instance

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
        data = super(IdentifierSerializer, self).to_representation(instance)

        links_instance = instance.links.untranslated().all()
        links_serializer = LinkSerializer(instance=links_instance, many=True, language=instance.language_code)
        data["links"] = links_serializer.data

        return data

    class Meta:
        model = Identifier
        exclude = ('object_id', 'content_type')
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class OtherNameSerializer(TranslatableModelSerializer):

    id = CharField(max_length=255, required=False)
    links = LinkSerializer(many=True, required=False)
    start_date = CharField(allow_null=True, default=None, allow_blank=True)
    end_date = CharField(allow_null=True, default=None, allow_blank=True)

    def create(self, validated_data):
        links = validated_data.pop('links', [])
        # Really where there language code come from!
        validated_data.pop("language_code", None)
        language = self.language
        if not "content_object" in validated_data:
            raise ContentObjectNotAvailable("Please save parent object by calling serializer.save(content_object=ParentObject)")
        if not validated_data.get("start_date"):
            validated_data["start_date"] = None

        if not validated_data.get("end_date"):
            validated_data["end_date"] = None

        othername = OtherName.objects.language(language).create(**validated_data)
        for link in links:
            self.create_links(link, othername)
        return othername

    def create_links(self, validated_data, entity):
        language_code = self.language
        validated_data["content_object"] = entity
        Link.objects.language(language_code).create(**validated_data)

    def update(self, instance, data):
        links = data.pop('links', [])
        instance.name = data.get('name', instance.name)
        instance.family_name = data.get('family_name', instance.family_name)
        instance.given_name = data.get('given_name', instance.given_name)
        instance.additional_name = data.get('additional_name', instance.additional_name)
        instance.honorific_suffix = data.get('honorific_suffix', instance.honorific_suffix)
        instance.honorific_prefix = data.get('honorific_prefix', instance.honorific_prefix)
        instance.patronymic_name = data.get('patronymic_name', instance.patronymic_name)
        instance.start_date = data.get('start_date', instance.start_date)
        if not instance.start_date:
            instance.start_date = None
        instance.end_date = data.get('end_date', instance.end_date)
        if not instance.end_date:
            instance.end_date = None
        instance.note = data.get('note', instance.note)

        instance.save()
        for link in links:
            self.update_links(link, instance)
        return instance

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
        data = super(OtherNameSerializer, self).to_representation(instance)

        links_instance = instance.links.untranslated().all()
        links_serializer = LinkSerializer(instance=links_instance, many=True, language=instance.language_code)
        data["links"] = links_serializer.data

        return data

    def validate_start_date(self, value):
        if not value:
            return value
        if not re.match(r"^[0-9]{4}(-[0-9]{2}){0,2}$", value):
            raise ValidationError("value need to be in ^[0-9]{4}(-[0-9]{2}){0,2}$ format")
        return value

    def validate_end_date(self, value):
        if not value:
            return value
        if not re.match(r"^[0-9]{4}(-[0-9]{2}){0,2}$", value):
            raise ValidationError("value need to be in ^[0-9]{4}(-[0-9]{2}){0,2}$ format")
        return value

    class Meta:
        model = OtherName
        exclude = ('object_id', 'content_type')
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class AreaSerializer(TranslatableModelSerializer):
    id = CharField(max_length=255, required=False)
    links = LinkSerializer(many=True, required=False)

    # Why create and update? Because we need to create an API endpoint to import data from mapit
    def create(self, validated_data):
        language = self.language
        validated_data.pop("language_code", None)
        parent_data = validated_data.pop("parent", {})
        links = validated_data.pop("links", [])

        if parent_data:
            if not "id" in parent_data:
                parent = self.create(parent_data)
            else:
                parent = self.update_area(parent_data)
            validated_data["parent"] = parent
        area = Area.objects.language(language).create(**validated_data)
        for link in links:
            self.create_links(link, area)

        return area

    def create_links(self, validated_data, parent):
        language_code = self.language
        validated_data["content_object"] = parent
        Link.objects.language(language_code).create(**validated_data)

    def update(self, instance, data):
        links = data.pop("links", [])
        language = self.language
        data.pop("language", None)
        instance.name = data.get("name", instance.name)
        instance.identifier = data.get("identifier", instance.identifier)
        instance.classification = data.get("classification", instance.classification)
        instance.save()

        for link in links:
            self.update_links(link, instance)
        return instance

    def update_area(self, data):
        # Raise excception if no id in field, it should be there
        area_id = data.pop("id")
        parent_data = data.pop("parent", None)
        links = data.pop('links', [])
        area = Area.objects.language(self.language).get(id=area_id)

        area.name = data.get('name', area.name)
        area.identifier = data.get('identifier', area.identifier)
        area.classification = data.get('classficiation', area.classification)
        if parent_data:
            if "id" in parent_data:
                parent = self.update_area(parent_data)
            else:
                parent = self.create(parent_data)
            area.parent = parent
        area.save()
        for link in links:
            self.update_links(link, area)
        return area

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
        data = super(AreaSerializer, self).to_representation(instance)

        links_instance = instance.links.untranslated().all()
        links_serializer = LinkSerializer(instance=links_instance, many=True, language=instance.language_code)
        data["links"] = links_serializer.data

        return data

    class Meta:
        model = Area
        extra_kwargs = {'id': {'read_only': False, 'required': False}}