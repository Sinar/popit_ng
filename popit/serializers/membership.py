from hvad.contrib.restframework import TranslatableModelSerializer
from rest_framework.serializers import CharField
from popit.models import Membership
from popit.models import Person
from popit.models import Organization
from popit.models import Area
from popit.models import Post
from popit.models import Link
from popit.models import ContactDetail
from popit.serializers import LinkSerializer
from popit.serializers import ContactDetailSerializer
from popit.serializers import AreaSerializer
from popit.serializers import OtherNameSerializer
from popit.serializers import IdentifierSerializer
from popit.serializers import OrganizationSerializer
from popit.serializers import PersonSerializer
from popit.serializers import PostSerializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError
import re
import logging


class MembershipPersonSerializer(TranslatableModelSerializer):
    id = CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    other_names = OtherNameSerializer(many=True, required=False)
    identifiers = IdentifierSerializer(many=True, required=False)
    birth_date = CharField(allow_null=True, default=None, allow_blank=True)
    death_date = CharField(allow_null=True, default=None, allow_blank=True)
    links = LinkSerializer(many=True, required=False)
    contact_details = ContactDetailSerializer(many=True, required=False)

    class Meta:
        model = Person
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class MembershipOrganizationSerializer(TranslatableModelSerializer):
    id = CharField(max_length=255, required=False,  allow_null=True, allow_blank=True)
    parent_id = CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    founding_date = CharField(allow_null=True, default=None, allow_blank=True)
    dissolution_date = CharField(allow_null=True, default=None, required=False, allow_blank=True)
    links = LinkSerializer(many=True, required=False)
    contact_details = ContactDetailSerializer(many=True, required=False)
    area = AreaSerializer(required=False)

    class Meta:
        model = Organization
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class MembershipPostSerializer(TranslatableModelSerializer):
    id = CharField(max_length=255, required=False)
    organization_id = CharField(max_length=255, required=False)
    area_id = CharField(max_length=255, required=False)
    start_date = CharField(allow_null=True, default=None)
    end_date = CharField(allow_null=True, default=None)
    contact_details = ContactDetailSerializer(many=True, required=False)
    links = LinkSerializer(many=True, required=False)

    class Meta:
        model = Post
        extra_kwargs = {'id': {'read_only': False, 'required': False}}
        exclude = [ "organization", "area"]


class MembershipSerializer(TranslatableModelSerializer):

    id = CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    person = MembershipPersonSerializer(required=False)
    person_id = CharField(max_length=255, required=False)
    organization = MembershipOrganizationSerializer(required=False)
    organization_id = CharField(max_length=255, required=False)
    member = MembershipOrganizationSerializer(required=False)
    member_id = CharField(max_length=255, required=False)
    on_behalf_of = MembershipOrganizationSerializer(required=False)
    on_behalf_of_id = CharField(max_length=255, required=False)
    area = AreaSerializer(required=False)
    area_id = CharField(max_length=255, required=False)
    post = MembershipPostSerializer(required=False)
    post_id = CharField(max_length=255, required=False)

    contact_details = ContactDetailSerializer(many=True, required=False)
    links = LinkSerializer(many=True, required=False)
    start_date = CharField(allow_null=True, default=None, allow_blank=True)
    end_date = CharField(allow_null=True, default=None, allow_blank=True)

    def create(self, validated_data):
        validated_data.pop("person", None)
        person_id = validated_data.pop("person_id", None)

        validated_data.pop("organization", None)
        organization_id = validated_data.pop("organization_id", None)

        validated_data.pop("on_half_of", None)
        on_behalf_of_id = validated_data.pop("on_half_of_id", None)

        validated_data.pop("area", None)
        area_id = validated_data.pop("area_id", None)

        validated_data.pop("post", None)
        post_id = validated_data.pop("post_id", None)

        contact_details = validated_data.pop("contact_details", [])
        links = validated_data.pop("links", [])
        validated_data.pop("language_code", None)

        if person_id:
            person = Person.objects.untranslated().get(id=person_id)
            validated_data["person"] = person

        if organization_id:
            organization = Organization.objects.untranslated().get(id=organization_id)
            validated_data["organization"] = organization

        if on_behalf_of_id:
            on_behalf_of = Organization.objects.untranslated().get(id=on_behalf_of_id)
            validated_data["on_behalf_of"] = on_behalf_of

        if area_id:
            area = Area.objects.untranslated().get(id=area_id)
            validated_data["area"] = area

        if post_id:
            post = Post.objects.untranslated().get(id=post_id)
            validated_data["post"] = post

            # Do not override organization assigned by user
            if not organization_id:
                if post.organization:
                    validated_data["organization"] = post.organization

        if not validated_data.get("start_date"):
            validated_data["start_date"] = None

        if not validated_data.get("end_date"):
            validated_data["end_date"] = None

        membership = Membership.objects.language(self.language).create(**validated_data)

        for contact_detail in contact_details:
            self.create_child(contact_detail, ContactDetail, membership)

        for link in links:
            self.create_links(link, membership)
        return membership

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
        available_languages = instance.get_available_languages()
        if not self.language in available_languages:
            instance = instance.translate(self.language)
        data.pop("person", None)
        person_id = data.pop("person_id", None)

        data.pop("organization", None)
        organization_id = data.pop("organization_id", None)

        data.pop("on_half_of", None)
        on_behalf_of_id = data.pop("on_half_of_id", None)

        data.pop("area", None)
        area_id = data.pop("area_id", None)

        data.pop("post", None)
        post_id = data.pop("post_id", None)

        contact_details = data.pop("contact_details", [])
        links = data.pop("links", [])
        data.pop("language_code", None)

        instance.label = data.get("label", instance.label)
        instance.role = data.get("role", instance.role)
        instance.start_date = data.get("start_date", instance.start_date)
        if not instance.start_date:
            instance.start_date = None
        instance.end_date = data.get("end_date", instance.end_date)
        if not instance.end_date:
            instance.end_date = None

        if person_id:
            person = Person.objects.untranslated().get(id=person_id)
            instance.person = person

        if organization_id:
            organization = Organization.objects.untranslated().get(id=organization_id)
            instance.organization = organization

        if on_behalf_of_id:
            on_behalf_of = Organization.objects.untranslated().get(id=on_behalf_of_id)
            instance.on_behalf_of = on_behalf_of

        if area_id:
            area = Area.objects.untranslated().get(id=area_id)
            instance.area = area

        if post_id:
            post = Post.objects.untranslated().get(id=post_id)
            instance.post = post

        instance.save()

        if instance.post:
            if not instance.organization:
                # The spec make this optional, but in sinar we link all post to org
                if instance.post.organization:
                    instance.organization = instance.post.organization
                    instance.save()

        for contact_detail in contact_details:

            self.update_childs(contact_detail, ContactDetail, instance)

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

    def validate(self, data):

        if not data.get("post_id") and not data.get("organization_id"):
            logging.warn(data)
            if not self.partial:
                raise serializers.ValidationError("Please provide either a post_id or organization_id when creating membership")

        if data.get("post_id"):
            try:
                Post.objects.untranslated().get(id=data.get("post_id"))
            except Post.DoesNotExist:
                raise ValidationError("Post id %s does not exist" % data.get("post_id"))

        if data.get("organization_id"):
            try:
                Organization.objects.untranslated().get(id=data.get("organization_id"))
            except Organization.DoesNotExist:
                raise ValidationError("Organization id %s does not exist" % data.get("organization_id"))

        if data.get("post_id") and data.get("organization_id"):
            post = Post.objects.untranslated().get(id=data.get("post_id"))
            if post.organization_id:
                if post.organization_id != data.get("organization_id"):
                    raise serializers.ValidationError("Organization id is not consistent orrganization id in post")

        if data.get("post_id") and not data.get("organization_id"):
            if self.instance:
                if self.instance.organization_id and self.instance.post.organization_id:
                    post = Post.objects.untranslated().get(id=data.get("post_id"))
                    if post.organization_id != self.instance.organization_id:
                        raise serializers.ValidationError("Post Organization ID does not match organization id")

        if not data.get("post_id") and data.get("organization_id"):
            if self.instance:
                if self.instance.post:
                    if self.instance.post.organization_id:
                        organization = Organization.objects.untranslated().get(id=data.get("organization_id"))
                        if organization.id != self.instance.post.organization_id:
                            raise serializers.ValidationError("Organization ID does not match Post Organization id")

        if data.get("area_id"):
            try:
                Area.objects.untranslated().get(id=data.get("area_id"))
            except Area.DoesNotExist:
                raise ValidationError("Area id %s does not exist" % data.get("area_id"))

        if data.get("start_date"):
            if not re.match(r"^[0-9]{4}(-[0-9]{2}){0,2}$", data.get("start_date")):
                raise serializers.ValidationError("value need to be in ^[0-9]{4}(-[0-9]{2}){0,2}$ format, currently %s" %
                                                  data.get("start_date"))

        if data.get("end_date"):
            if not re.match(r"^[0-9]{4}(-[0-9]{2}){0,2}$", data.get("end_date")):
                raise serializers.ValidationError("value need to be in ^[0-9]{4}(-[0-9]{2}){0,2}$ format, currently %s" %
                                                  data.get("end_date"))

        if not data.get("person_id"):
            if not self.partial:
                raise serializers.ValidationError("person_id must not be empty")
        else:
            try:
                Person.objects.untranslated().get(id=data.get("person_id"))

            except Person.DoesNotExist:
                raise serializers.ValidationError("Person %s does not exist" % data.get("person_id"))


        return data

    def to_representation(self, instance):
        data = super(MembershipSerializer, self).to_representation(instance)
        # Now we do all the overriding

        if instance.organization_id:
            organization_instance = instance.organization.__class__.objects.untranslated().get(id=instance.organization_id)
            organization_serializer = MembershipOrganizationSerializer(instance=organization_instance, language=instance.language_code)
            data["organization"] = organization_serializer.data

        if instance.on_behalf_of_id:
            on_behalf_of_instance = instance.on_behalf_of.__class__.objects.untranslated().get(id=instance.on_behalf_of_id)
            on_behalf_of_serializer = MembershipOrganizationSerializer(on_behalf_of_instance, language=instance.language_code)
            data["on_behalf_of"] = on_behalf_of_serializer.data

        if instance.member_id:
            member_instance = instance.member.__class__.objects.untranslated().get(id=instance.member_id)
            member_serializer = MembershipOrganizationSerializer(instance=member_instance, language=instance.language_code)
            data["member"] = member_serializer.data

        person_instance = instance.person.__class__.objects.untranslated().get(id=instance.person_id)
        person_serializer = MembershipPersonSerializer(instance=person_instance, language=instance.language_code)
        data["person"] = person_serializer.data

        if instance.post_id:
            post_instance = instance.post.__class__.objects.untranslated().get(id=instance.post_id)
            post_serializer = MembershipPostSerializer(instance=post_instance, language=instance.language_code)
            data["post"] = post_serializer.data

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
        return data

    class Meta:
        model = Membership
        extra_kwargs = {'id': {'read_only': False, 'required': False}}