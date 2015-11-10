__author__ = 'sweemeng'
from popit.models import Organization
from popit.models import ContactDetail
from popit.models import Link
from popit.models import Identifier
from popit.models import OtherName
from popit.models import Area
from hvad.contrib.restframework import TranslatableModelSerializer
from rest_framework.serializers import CharField
from popit.serializers.misc import OtherNameSerializer
from popit.serializers.misc import IdentifierSerializer
from popit.serializers.misc import LinkSerializer
from popit.serializers.misc import ContactDetailSerializer
from popit.serializers.misc import AreaSerializer

# We make this read only, and we shall show 1 level of parent. Not grand parent
class ParentOrganizationSerializer(TranslatableModelSerializer):
    id = CharField(max_length=255, required=False)
    other_names = OtherNameSerializer(many=True, required=False)
    identifiers = IdentifierSerializer(many=True, required=False)
    links = LinkSerializer(many=True, required=False)
    contact_details = ContactDetailSerializer(many=True, required=False)
    area = AreaSerializer(required=False)

    class Meta:
        model = Organization
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class OrganizationSerializer(TranslatableModelSerializer):

    id = CharField(max_length=255, required=False)
    parent = ParentOrganizationSerializer(required=False)
    parent_id = CharField(max_length=255, required=False)
    other_names = OtherNameSerializer(many=True, required=False)
    identifiers = IdentifierSerializer(many=True, required=False)
    links = LinkSerializer(many=True, required=False)
    contact_details = ContactDetailSerializer(many=True, required=False)
    area = AreaSerializer(required=False)
    area_id = CharField(max_length=255, required=False)

    def create(self, validated_data):
        other_names = validated_data.pop('other_names', [])
        links = validated_data.pop('links', [])
        identifiers = validated_data.pop('identifier', [])
        contact_details = validated_data.pop('contact_details', [])
        language = self.language
        validated_data.pop("language_code", None)

        validated_data.pop("parent", None)

        area_data = validated_data.pop("area", None)
        area_id = validated_data.pop("area_id", None)
        # We can only assign parent and area, not create it.
        # Except there is no area database in popit
        # Also what if area_id do not exist
        area = None
        if area_id:
            try:
                area = Area.objects.untranslated().get(id=area_id)
                validated_data["area"] = area
            except Area.DoesNotExist:
                area = None

        if area_data:
            if not area:
                area = self.create_area(area_data)
                validated_data["area"] = area


        parent_id = validated_data.pop("parent_id", None)

        if parent_id:
            parent_org = Organization.objects.untranslated().get(id=parent_id)
            validated_data["parent"] = parent_org
        organization = Organization.objects.language(language).create(**validated_data)
        for other_name in other_names:
            self.create_child(other_name, OtherName, organization)

        for link in links:
            self.create_links(link, organization)

        for identifier in identifiers:
            self.create_child(identifier, Identifier, organization)

        for contact in contact_details:
            self.create_child(contact, ContactDetail, organization)

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

    def create_area(self, validated_data):
        language_code = self.language
        validated_data.pop("language_code", None)
        area = Area.objects.language(language_code).create(**validated_data)
        return area

    def update(self, instance, data):
        other_names = data.pop("other_names", [])
        links = data.pop("links", [])
        identifiers = data.pop("identifiers", [])
        contact_details = data.pop("contact_details", [])
        area = data.pop("area", None)
        area_id = data.pop("area_id", None)

        parent = data.pop("parent", None)
        parent_id = data.pop("parent_id", None)

        instance.name = data.get("name", instance.name)
        instance.classification = data.get("classification", instance.classification)
        instance.abstract = data.get("abstract", instance.abstract)
        instance.description = data.get("description", instance.description)
        instance.founding_date = data.get("founding_date", instance.founding_date)
        instance.dissolution_date = data.get("dissolution_date", instance.dissolution_date)

        # We only allow pointing to new parent and area not create a new parent and area
        if area_id:
            try:
                area = Area.objects.language(instance.language_code).get(id=area_id)
                instance.area = area
            except Area.DoesNotExist:
                pass

        if parent_id:
            try:
                parent = Organization.objects.language(instance.language_code).get(id=parent_id)
                instance.parent = parent
            except Organization.DoesNotExist:
                pass

        instance.save()

        for other_name in other_names:
            self.update_childs(other_name, OtherName, instance)

        for identifier in identifiers:
            self.update_childs(identifier, Identifier, instance)

        for contact in contact_details:
            self.update_childs(contact, ContactDetail, instance)

        for link in links:
            self.update_links(link, instance)

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

    class Meta:
        model = Organization
        extra_kwargs = {'id': {'read_only': False, 'required': False}}