__author__ = 'sweemeng'
from popit.models import Person
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

class PersonSerializer(TranslatableModelSerializer):

    id = CharField(max_length=255, required=False)
    other_names = OtherNameSerializer(many=True, required=False)
    identifiers = IdentifierSerializer(many=True, required=False)
    links = LinkSerializer(many=True, required=False)
    contacts = ContactSerializer(many=True, required=False)

    def create(self, validated_data):
        language_code=self.language
        links = validated_data.pop("links")
        other_names = validated_data.pop("other_names")
        contacts = validated_data.pop('contacts')
        identifiers = validated_data.pop("identifiers")
        # Where do the language come from inside the create function
        validated_data.pop("language_code", [])
        person = Person.objects.language(language_code).create(**validated_data)

        for other_name in other_names:
            self.create_child(other_name, OtherName, person)

        for contact in contacts:
            self.create_child(contact, Contact, person)

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
        instance.death_date = validated_data.get("death_date", instance.death_date)
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

        contacts = validated_data.pop("contacts", [])
        for contact in contacts:
            self.update_childs(contact, Contact, instance)

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

    class Meta:
        model = Person
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


