__author__ = 'sweemeng'
from hvad.contrib.restframework import TranslatableModelSerializer
from popit.models import Post
from popit.models import Link
from popit.models import Area
from popit.models import OtherName
from popit.models import Organization
from popit.models import Contact
from rest_framework.serializers import CharField
from popit.serializers.organization import OrganizationSerializer
from popit.serializers.misc import OtherNameSerializer
from popit.serializers.misc import LinkSerializer
from popit.serializers.misc import ContactSerializer
from popit.serializers.misc import AreaSerializer


class PostSerializer(TranslatableModelSerializer):

    id = CharField(max_length=255, required=False)
    other_labels = OtherNameSerializer(many=True, required=False)
    organization = OrganizationSerializer(required=False) # A post must tied to an organization
    organization_id = CharField(max_length=255)
    area = AreaSerializer(required=False)
    area_id = CharField(max_length=255, required=False)

    contact_details = ContactSerializer(many=True, required=False)
    links = LinkSerializer(many=True, required=False)

    def create(self, validated_data):
        other_labels = validated_data.pop("other_labels", [])
        validated_data.pop("organization", {})
        organization_id = validated_data.pop("organization_id", None)
        validated_data.pop("area", {})
        area_id = validated_data.pop("area_id", None)
        links = validated_data.pop("links", [])
        contacts = validated_data.pop("contacts", [])
        validated_data.pop("language_code", None)

        # Organization is read and assign only, no create or update
        organization = Organization.objects.language(self.language).get(id=organization_id)
        validated_data["organization"] = organization

        # Area in this object is link or read only, not create or update
        if area_id:
            area = Area.objects.language(self.language).get(id=area_id)
            validated_data["area"] = area

        post = Post.objects.language(self.language).create(**validated_data)

        for other_label in other_labels:
            self.create_child(other_label, OtherName, post)

        for link in links:
            self.create_links(link, post)

        for contact in contacts:
            self.create_child(contact, Contact, post)

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


        instance.label = data.get("label", instance.label)
        instance.role = data.get("role", instance.role)

        instance.start_date = data.get("start_date", instance.start_date)
        instance.end_date = data.get("end_date", instance.end_date)
        if data.get("area_id"):
            area = Area.objects.language(self.language).get(id=data.get("area_id"))
            instance.area = area

        if data.get("organization_id"):
            organization = Organization.objects.language(self.language).get(id=data.get("area_id"))
            instance.organization = organization

        instance.save()

        other_labels = data.get("other_labels", [])

        for other_label in other_labels:
            self.update_childs(other_label, OtherName, instance)

        contacts_details = data.get("contact_details", [])

        for contact_detail in contacts_details:
            self.update_childs(contact_detail, Contact, instance)

        links = data.get("links", [])

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
        model = Post
        extra_kwargs = {'id': {'read_only': False, 'required': False}}
