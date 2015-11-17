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
from popit.serializers import OrganizationSerializer
from popit.serializers import PersonSerializer
from popit.serializers import PostSerializer
from rest_framework import serializers


class MembershipSerializer(TranslatableModelSerializer):

    id = CharField(max_length=255, required=False)
    person = PersonSerializer(required=False)
    person_id = CharField(max_length=255, required=False)
    organization = OrganizationSerializer(required=False)
    organization_id = CharField(max_length=255, required=False)
    member = OrganizationSerializer(required=False)
    member_id = CharField(max_length=255, required=False)
    on_behalf_of = OrganizationSerializer(required=False)
    on_behalf_of_id = CharField(max_length=255, required=False)
    area = AreaSerializer(required=False)
    area_id = CharField(max_length=255, required=False)
    post = PostSerializer(required=False)
    post_id = CharField(max_length=255, required=False)

    contact_details = ContactDetailSerializer(many=True, required=False)
    links = LinkSerializer(many=True, required=False)

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
            person = Person.objects.language(self.language).get(id=person_id)
            validated_data["person"] = person

        if organization_id:
            organization = Organization.objects.language(self.language).get(id=organization_id)
            validated_data["organization"] = organization

        if on_behalf_of_id:
            on_behalf_of = Organization.objects.language(self.language).get(id=on_behalf_of_id)
            validated_data["on_behalf_of"] = on_behalf_of

        if area_id:
            area = Area.objects.language(self.language).get(id=area_id)
            validated_data["area"] = area

        if post_id:
            post = Post.objects.language(self.language).get(id=post_id)
            validated_data["post"] = post

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
        instance.end_date = data.get("end_date", instance.end_date)

        if person_id:
            person = Person.objects.language(self.language).get(id=person_id)
            instance.person = person

        if organization_id:
            organization = Organization.objects.language(self.language).get(id=organization_id)
            instance.organization = organization

        if on_behalf_of_id:
            on_behalf_of = Organization.objects.language(self.language).get(id=on_behalf_of_id)
            instance.on_behalf_of = on_behalf_of

        if area_id:
            area = Area.objects.language(self.language).get(id=area_id)
            instance.area = area

        if post_id:
            post = Post.objects.language(self.language).get(id=post_id)
            instance.post = post

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
            if not self.partial:

                raise serializers.ValidationError("Please provide either a post_id or organization_id when creating membership")
        if data.get("post_id") and data.get("organization_id"):
            post = Post.objects.untranslated().get(id=data.get("post_id"))
            if post.organization_id != data.get("organization_id"):
                raise serializers.ValidationError("Organization id is not consistent orrganization id in post")

        if data.get("post_id") and not data.get("organization_id"):
            if self.instance:
                if self.instance.organization_id:
                    post = Post.objects.untranslated().get(id=data.get("post_id"))
                    if post.organization_id != self.instance.organization_id:
                        raise serializers.ValidationError("Post Organization ID does not match organization id")

        if not data.get("post_id") and data.get("organization_id"):
            if self.instance:
                if self.instance.post:
                    organization = Organization.objects.untranslated().get(id=data.get("organization_id"))
                    if organization.id != self.instance.post.organization_id:
                        raise serializers.ValidationError("Organization ID does not match Post Organization id")
        return data


    class Meta:
        model = Membership
        extra_kwargs = {'id': {'read_only': False, 'required': False}}