from hvad.contrib.restframework import TranslatableModelSerializer
from rest_framework.serializers import CharField
from popit.models import Relation
from popit.models import Person
from popit.models import Link
from popit.serializers import LinkSerializer
from popit.serializers import ContactDetailSerializer
from popit.serializers import OtherNameSerializer
from popit.serializers import IdentifierSerializer
from popit.serializers.base import BasePopitSerializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError
import re
import logging


class RelationPersonSerializer(TranslatableModelSerializer):
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

class RelationSerializer(BasePopitSerializer):

    id = CharField(max_length=255, required=False, allow_null=True, allow_blank=True)
    object = RelationPersonSerializer(required=False)
    object_id = CharField(max_length=255, required=False)
    subject = RelationPersonSerializer(required=False)
    subject_id = CharField(max_length=255, required=False)

    links = LinkSerializer(many=True, required=False)
    start_date = CharField(allow_null=True, default=None, allow_blank=True)
    end_date = CharField(allow_null=True, default=None, allow_blank=True)

    def create(self, validated_data):
        validated_data.pop("object", None)
        object_id = validated_data.pop("object_id", None)
        validated_data.pop("subject", None)
        subject_id = validated_data.pop("subject_id", None)

        links = validated_data.pop("links", [])
        validated_data.pop("language_code", None)

        if object_id:
            object = Person.objects.untranslated().get(id=object_id)
            validated_data["object"] = object
        if subject_id:
            subject = Person.objects.untranslated().get(id=subject_id)
            validated_data["subject"] = subject

        if not validated_data.get("start_date"):
            validated_data["start_date"] = None

        if not validated_data.get("end_date"):
            validated_data["end_date"] = None

        relation = Relation.objects.language(self.language).create(**validated_data)

        for link in links:
            self.create_links(link, relation)
        return relation

    def update(self, instance, data):
        available_languages = instance.get_available_languages()
        if not self.language in available_languages:
            instance = instance.translate(self.language)
        data.pop("object", None)
        object_id = data.pop("object_id", None)
        data.pop("subject", None)
        subject_id = data.pop("subject_id", None)

        links = data.pop("links", [])
        data.pop("language_code", None)

        instance.label = data.get("label", instance.label)
        instance.start_date = data.get("start_date", instance.start_date)
        if not instance.start_date:
            instance.start_date = None
        instance.end_date = data.get("end_date", instance.end_date)
        if not instance.end_date:
            instance.end_date = None

        if object_id:
            object = Person.objects.untranslated().get(id=object_id)
            instance.object = object
        if subject_id:
            subject = Person.objects.untranslated().get(id=subject_id)
            instance.subject = subject
        instance.save()

        for link in links:
            self.update_links(link, instance)

        return instance

    def validate(self, data):

        if data.get("start_date"):
            if not re.match(r"^[0-9]{4}(-[0-9]{2}){0,2}$", data.get("start_date")):
                raise serializers.ValidationError("value need to be in ^[0-9]{4}(-[0-9]{2}){0,2}$ format, currently %s" %
                                                  data.get("start_date"))

        if data.get("end_date"):
            if not re.match(r"^[0-9]{4}(-[0-9]{2}){0,2}$", data.get("end_date")):
                raise serializers.ValidationError("value need to be in ^[0-9]{4}(-[0-9]{2}){0,2}$ format, currently %s" %
                                                  data.get("end_date"))

        if not data.get("object_id"):
            if not self.partial:
                raise serializers.ValidationError("object_id must not be empty")
        else:
            try:
                Person.objects.untranslated().get(id=data.get("object_id"))
            except Person.DoesNotExist:
                raise serializers.ValidationError("Person %s does not exist" % data.get("object_id"))
        if not data.get("subject_id"):
            if not self.partial:
                raise serializers.ValidationError("subject_id must not be empty")
        else:
            try:
                Person.objects.untranslated().get(id=data.get("subject_id"))
            except Person.DoesNotExist:
                raise serializers.ValidationError("Person %s does not exist" % data.get("subject_id"))

        if not self.partial:
            if data.get("object_id") == data.get("subject_id"):
                raise serializers.ValidationError("object_id and subject_id must not be the same")
        elif data.get("object_id"):
            if data.get("object_id") == self.instance.subject_id:
                raise serializers.ValidationError("object_id and subject_id must not be the same")
        elif data.get("subject_id"):
            if data.get("subject_id") == self.instance.object_id:
                raise serializers.ValidationError("object_id and subject_id must not be the same")

        return data

    def to_representation(self, instance):
        data = super(RelationSerializer, self).to_representation(instance)
        # Now we do all the overriding

        object_instance = instance.object.__class__.objects.untranslated().get(id=instance.object_id)
        object_serializer = RelationPersonSerializer(instance=object_instance, language=instance.language_code)
        data["object"] = object_serializer.data
        subject_instance = instance.subject.__class__.objects.untranslated().get(id=instance.subject_id)
        subject_serializer = RelationPersonSerializer(instance=subject_instance, language=instance.language_code)
        data["subject"] = subject_serializer.data

        links_instance = instance.links.untranslated().all()
        links_serializer = LinkSerializer(instance=links_instance, many=True, language=instance.language_code)
        data["links"] = links_serializer.data

        return data

    class Meta:
        model = Relation
        extra_kwargs = {'id': {'read_only': False, 'required': False}}
