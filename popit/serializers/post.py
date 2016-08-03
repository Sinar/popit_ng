__author__ = 'sweemeng'
from hvad.contrib.restframework import TranslatableModelSerializer
from popit.models import Post
from popit.models import Person
from popit.models import Link
from popit.models import Area
from popit.models import OtherName
from popit.models import Organization
from popit.models import ContactDetail
from popit.models import Membership
from rest_framework.serializers import CharField
from popit.serializers.organization import OrganizationSerializer
from popit.serializers.misc import OtherNameSerializer
from popit.serializers.misc import LinkSerializer
from popit.serializers.misc import ContactDetailSerializer
from popit.serializers.misc import AreaSerializer
from popit.serializers.flat import PersonFlatSerializer
from popit.serializers.flat import OrganizationFlatSerializer
from popit.serializers.flat import PostFlatSerializer
import re
from rest_framework.serializers import ValidationError
from popit.serializers.misc import IdentifierSerializer


class PostMembershipSerializer(TranslatableModelSerializer):

    id = CharField(max_length=255, required=False)
    person_id = CharField(max_length=255, required=False)
    person = PersonFlatSerializer(required=False)
    organization_id = CharField(max_length=255, required=False)
    organization = OrganizationFlatSerializer(required=False)
    member_id = CharField(max_length=255, required=False)
    on_behalf_of_id = CharField(max_length=255, required=False)
    area_id = CharField(max_length=255, required=False, allow_null=True)
    post_id = CharField(max_length=255, required=False)
    post = PostFlatSerializer(required=False)

    contact_details = ContactDetailSerializer(many=True, required=False)
    links = LinkSerializer(many=True, required=False)
    start_date = CharField(allow_null=True, default=None)
    end_date = CharField(allow_null=True, default=None)

    def to_representation(self, instance):
        data = super(PostMembershipSerializer, self).to_representation(instance)

        person = Person.objects.untranslated().get(id=instance.person_id)
        person_serializer = PersonFlatSerializer(person, language=instance.language_code)

        data["person"] = person_serializer.data

        # Now all organization saved should have organization, either derived from post, or assigned directly
        if instance.organization:
            organization = Organization.objects.untranslated().get(id=instance.organization_id)
            organization_serializer = OrganizationFlatSerializer(organization, language=instance.language_code)
            data["organization"] = organization_serializer.data

        contact_details = instance.contact_details.untranslated().all()
        contact_details_serializer = ContactDetailSerializer(contact_details, many=True, language=instance.language_code)

        data["contact_details"] = contact_details_serializer.data

        links = instance.links.untranslated().all()
        links_serializer = LinkSerializer(links, many=True, language=instance.language_code)
        data["links"] = links_serializer.data
        return data

    class Meta:
        model = Membership
        extra_kwargs = {'id': {'read_only': False, 'required': False}}
        exclude = ["area"]


class PostParentOrganizationSerializer(TranslatableModelSerializer):
    id = CharField(max_length=255, required=False)
    other_names = OtherNameSerializer(many=True, required=False)
    identifiers = IdentifierSerializer(many=True, required=False)
    links = LinkSerializer(many=True, required=False)
    contact_details = ContactDetailSerializer(many=True, required=False)
    area = AreaSerializer(required=False)

    def to_representation(self, instance):
        data = super(PostParentOrganizationSerializer, self).to_representation(instance)

        other_names = instance.other_names.untranslated().all()
        other_names_serializer = OtherNameSerializer(other_names, many=True, language=instance.language_code)
        data["other_names"] = other_names_serializer.data

        identifiers = instance.identifiers.untranslated().all()
        identifiers_serializer = IdentifierSerializer(identifiers, many=True, language=instance.language_code)
        data["identifiers"] = identifiers_serializer.data

        contact_details = instance.contact_details.untranslated().all()
        contact_details_serializer = ContactDetailSerializer(contact_details, many=True, language=instance.language_code)
        data["contact_details"] = contact_details_serializer.data

        links = instance.links.untranslated().all()
        links_serializer = LinkSerializer(links, many=True, language=instance.language_code)
        data["links"] = links_serializer.data

        if instance.area:
            area = Area.objects.untranslated().get(id=instance.area_id)
            area_serializer = AreaSerializer(area, language=instance.language_code)
            data["area"] = area_serializer.data

        return data

    class Meta:
        model = Organization
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class PostOrganizationSerializer(TranslatableModelSerializer):
    id = CharField(max_length=255, required=False,  allow_null=True, allow_blank=True)
    parent = PostParentOrganizationSerializer(required=False)
    parent_id = CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    other_names = OtherNameSerializer(many=True, required=False)
    identifiers = IdentifierSerializer(many=True, required=False)
    links = LinkSerializer(many=True, required=False)
    contact_details = ContactDetailSerializer(many=True, required=False)
    area = AreaSerializer(required=False)
    area_id = CharField(max_length=255, required=False)
    founding_date = CharField(allow_null=True, default=None, allow_blank=True)
    dissolution_date = CharField(allow_null=True, default=None, required=False, allow_blank=True)

    def to_representation(self, instance):
        data = super(PostOrganizationSerializer, self).to_representation(instance)
        if instance.parent:
            parent = Organization.objects.untranslated().get(id=instance.parent_id)
            parent_serializer = PostParentOrganizationSerializer(parent, language=instance.language_code)
            data["parent"] = parent_serializer.data

        other_names = instance.other_names.untranslated().all()
        other_names_serializer = OtherNameSerializer(other_names, many=True, language=instance.language_code)
        data["other_names"] = other_names_serializer.data

        identifiers = instance.identifiers.untranslated().all()
        identifiers_serializer = IdentifierSerializer(identifiers, many=True, language=instance.language_code)
        data["identifiers"] = identifiers_serializer.data

        contact_details = instance.contact_details.untranslated().all()
        contact_details_serializer = ContactDetailSerializer(contact_details, many=True, language=instance.language_code)
        data["contact_details"] = contact_details_serializer.data

        if instance.area:

            area = Area.objects.untranslated().get(id=instance.area_id)
            area_serializer = AreaSerializer(area, language=instance.language_code)
            data["area"] = area_serializer.data

        return data

    class Meta:
        model = Organization
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class PostSerializer(TranslatableModelSerializer):

    id = CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    label = CharField(max_length=255, required=False)
    other_labels = OtherNameSerializer(many=True, required=False)
    organization = PostOrganizationSerializer(required=False) # A post must tied to an organization
    organization_id = CharField(max_length=255, required=False)
    area = AreaSerializer(required=False)
    area_id = CharField(max_length=255, required=False)

    memberships = PostMembershipSerializer(required=False, many=True)

    contact_details = ContactDetailSerializer(many=True, required=False)
    links = LinkSerializer(many=True, required=False)
    start_date = CharField(allow_null=True, default=None, allow_blank=True)
    end_date = CharField(allow_null=True, default=None, allow_blank=True)


    def create(self, validated_data):
        other_labels = validated_data.pop("other_labels", [])
        validated_data.pop("organization", {})
        organization_id = validated_data.pop("organization_id", None)
        validated_data.pop("area", {})
        area_id = validated_data.pop("area_id", None)
        links = validated_data.pop("links", [])
        contacts = validated_data.pop("contact_details", [])
        validated_data.pop("language_code", None)
        validated_data.pop("memberships", None)

        # Organization is read and assign only, no create or update
        if organization_id:
            organization = Organization.objects.untranslated().get(id=organization_id)
            validated_data["organization"] = organization

        # Area in this object is link or read only, not create or update
        if area_id:
            area = Area.objects.untranslated().get(id=area_id)
            validated_data["area"] = area

        if not validated_data.get("start_date"):
            validated_data["start_date"] = None

        if not validated_data.get("end_date"):
            validated_data["end_date"] = None

        post = Post.objects.language(self.language).create(**validated_data)

        for other_label in other_labels:
            self.create_child(other_label, OtherName, post)

        for link in links:
            self.create_links(link, post)

        for contact in contacts:
            self.create_child(contact, ContactDetail, post)

        return post

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
        available_language = instance.get_available_languages()
        if not self.language in available_language:
            instance = instance.translate(self.language)

        instance.label = data.get("label", instance.label)
        instance.role = data.get("role", instance.role)

        instance.start_date = data.get("start_date", instance.start_date)
        if not instance.start_date:
            instance.start_date = None

        instance.end_date = data.get("end_date", instance.end_date)
        if not instance.end_date:
            instance.end_date = None

        if data.get("area_id"):
            area = Area.objects.untranslated().get(id=data.get("area_id"))
            instance.area = area

        if data.get("organization_id"):
            organization = Organization.objects.untranslated().get(id=data.get("area_id"))
            instance.organization = organization

        instance.save()

        other_labels = data.get("other_labels", [])

        for other_label in other_labels:
            self.update_childs(other_label, OtherName, instance)

        contacts_details = data.get("contact_details", [])

        for contact_detail in contacts_details:
            self.update_childs(contact_detail, ContactDetail, instance)

        links = data.get("links", [])

        for link in links:
            self.update_links(link, instance)

        return instance

    def update_childs(self, validated_data, child, parent):
        # parent mostly exist at create,
        language_code = self.language
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
        language_code = self.language

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
        data = super(PostSerializer, self).to_representation(instance)
        # Now we do all the overriding
        other_labels = instance.other_labels.untranslated().all()
        if other_labels:
            other_labels_serializer = OtherNameSerializer(instance=other_labels, language=instance.language_code, many=True)
            data["other_labels"] = other_labels_serializer.data
        else:
            data["other_labels"] = []

        if instance.organization:
            organization_instance = Organization.objects.untranslated().get(id=instance.organization_id)
            organization_serializer = PostOrganizationSerializer(instance=organization_instance, language=instance.language_code)
            data["organization"] = organization_serializer.data

        links_instance = instance.links.untranslated().all()
        links_serializer = LinkSerializer(instance=links_instance, many=True, language=instance.language_code)
        data["links"] = links_serializer.data

        contact_details_instance = instance.contact_details.untranslated().all()
        contact_details_serializer = ContactDetailSerializer(instance=contact_details_instance, many=True,
                                                             language=instance.language_code)
        data["contact_details"] = contact_details_serializer.data

        if instance.area_id:
            area_instance = instance.area.__class__.objects.untranslated().get(id=instance.area_id)
            area_serializer = AreaSerializer(area_instance, language=instance.language_code)
            data["area"] = area_serializer.data

        memberships = instance.memberships.untranslated().all()
        memberships_serializer = PostMembershipSerializer(memberships, many=True, language=instance.language_code)
        data["memberships"] = memberships_serializer.data
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

    def validate_area_id(self, value):
        if not value:
            return value
        try:
            Area.objects.untranslated().get(id=value)
        except Area.DoesNotExist:
            raise ValidationError("Area id %s does not exist" % value)
        return value

    def validate_organization_id(self, value):
        if not value:
            return value

        try:
            Organization.objects.untranslated().get(id=value)
        except Organization.DoesNotExist:
            raise ValidationError("Organization id %s Does not exist" % value)
        return value

    class Meta:
        model = Post
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


