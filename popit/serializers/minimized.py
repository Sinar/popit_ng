__author__ = 'sweemeng'
from popit.models import Person
from popit.models import Organization
from popit.models import Post
from popit.models import Membership
from popit.models import Relation
from popit.models import ContactDetail
from popit.models import Link
from popit.models import Identifier
from popit.models import OtherName
from hvad.contrib.restframework import TranslatableModelSerializer
from popit.serializers.base import BasePopitSerializer
from popit.serializers.misc import OtherNameSerializer
from popit.serializers.misc import IdentifierSerializer
from popit.serializers.misc import LinkSerializer
from popit.serializers.misc import ContactDetailSerializer
from rest_framework.serializers import PrimaryKeyRelatedField


# Why not flat? Because it is not truly flat, we just remove some relationship, but not all
# This is mostly read only we won't be writing data to this
class MinPersonSerializer(TranslatableModelSerializer):
    other_names = OtherNameSerializer(many=True, required=False)
    identifiers = IdentifierSerializer(many=True, required=False)
    links = LinkSerializer(many=True, required=False)
    contact_details = ContactDetailSerializer(many=True, required=False)
    memberships = PrimaryKeyRelatedField(many=True, read_only=True)
 
    class Meta:
        model = Person
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class MinOrganizationSerializer(TranslatableModelSerializer):
    other_names = OtherNameSerializer(many=True, required=False)
    identifiers = IdentifierSerializer(many=True, required=False)
    links = LinkSerializer(many=True, required=False)
    contact_details = ContactDetailSerializer(many=True, required=False)
    memberships = PrimaryKeyRelatedField(many=True, read_only=True)
 
    class Meta:
        model = Organization
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class MinMembershipSerializer(TranslatableModelSerializer):
    links = LinkSerializer(many=True, required=False)
    contact_details = ContactDetailSerializer(many=True, required=False)

    class Meta:
        model = Membership
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class MinRelationSerializer(TranslatableModelSerializer):
    links = LinkSerializer(many=True, required=False)

    class Meta:
        model = Relation
        extra_kwargs = {'id': {'read_only': False, 'required': False}}


class MinPostSerializer(TranslatableModelSerializer):
    other_labels = OtherNameSerializer(many=True, required=False)
    links = LinkSerializer(many=True, required=False)
    contact_details = ContactDetailSerializer(many=True, required=False)
    memberships = PrimaryKeyRelatedField(many=True, read_only=True)
 
    class Meta:
        model = Post
        extra_kwargs = {'id': {'read_only': False, 'required': False}}

