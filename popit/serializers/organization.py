__author__ = 'sweemeng'
from popit.models import Organization
from popit.models import Contact
from popit.models import Link
from popit.models import Identifier
from popit.models import OtherName
from hvad.contrib.restframework import TranslatableModelSerializer
from rest_framework.serializers import CharField
from popit.serializers.misc import OtherNameSerializer
from popit.serializers.misc import IdentifierSerializer
from popit.serializers.misc import LinkSerializer
from popit.serializers.misc import ContactSerializer
from popit.serializers.misc import AreaSerializer


class OrganizationSerializer(TranslatableModelSerializer):

    id = CharField(max_length=255, required=False)
    other_names = OtherNameSerializer(many=True, required=False)
    identifiers = IdentifierSerializer(many=True, required=False)
    links = LinkSerializer(many=True, required=False)
    contacts = ContactSerializer(many=True, required=False)
    area = AreaSerializer(required=False)

    def create(self, validated_data):
        other_names = validated_data.pop('other_names', [])
        links = validated_data.pop('links', [])
        identifiers = validated_data.pop('identifier', [])
        contacts = validated_data.pop('contacts', [])
        language = self.language
        validated_data.pop("language_code", None)
        organization = Organization.objects.language(language).create(**validated_data)
        for other_name in other_names:
            self.create_child(other_name, OtherName, organization)

        for link in links:
            self.create(link, Link, organization)

        for identifier in identifiers:
            self.create_child(identifier, Identifier, organization)

        for contact in contacts:
            self.create_child(contact, Contact, organization)

        return organization

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

    def update(self, instance, data):
        language = self.language
        other_names = data.pop("other_names", [])
        links = data.pop("links", [])
        identifiers = data.pop("identifiers", [])
        contacts = data.pop("contacts", [])

        instance.name = data.get("name", instance.name)
        instance.classification = data.get("classification", instance.classification)



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

    class Meta:
        model = Organization
        extra_kwargs = {'id': {'read_only': False, 'required': False}}