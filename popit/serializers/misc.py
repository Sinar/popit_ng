__author__ = 'sweemeng'
from popit.models import Person
from popit.models import Contact
from popit.models import Link
from popit.models import Identifier
from popit.models import OtherName
from hvad.contrib.restframework import TranslatableModelSerializer
from rest_framework.serializers import CharField
from popit.serializers.exceptions import ContentObjectNotAvailable


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


class ContactSerializer(TranslatableModelSerializer):

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
        contact = Contact.objects.language(language).create(
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

    class Meta:
        model = Contact
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

    class Meta:
        model = Identifier
        exclude = ('object_id', 'content_type')
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class OtherNameSerializer(TranslatableModelSerializer):

    id = CharField(max_length=255, required=False)
    links = LinkSerializer(many=True, required=False)

    def create(self, validated_data):
        links = validated_data.pop('links', [])
        # Really where there language code come from!
        validated_data.pop("language_code", None)
        language = self.language
        if not "content_object" in validated_data:
            raise ContentObjectNotAvailable("Please save parent object by calling serializer.save(content_object=ParentObject)")
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
        instance.end_date = data.get('end_date', instance.end_date)

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

    class Meta:
        model = OtherName
        exclude = ('object_id', 'content_type')
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


