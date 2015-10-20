__author__ = 'sweemeng'
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import Http404
from popit.serializers import PersonSerializer
from popit.models import Person
from popit.serializers import ContactSerializer
from popit.serializers import LinkSerializer
from popit.serializers import IdentifierSerializer
from popit.serializers import OtherNameSerializer
from popit.serializers.exceptions import ChildNotSetException
from popit.models import Person
from popit.models import Contact
from popit.models import Link
from popit.models import OtherName
from popit.models import Identifier
from popit.views.misc import GenericContactDetail
from popit.views.misc import GenericContactLinkDetail
from popit.views.misc import GenericContactLinkList
from popit.views.misc import GenericContactList
from popit.views.misc import GenericIdentifierDetail
from popit.views.misc import GenericIdentifierLinkDetail
from popit.views.misc import GenericIdentifierLinkList
from popit.views.misc import GenericIdentifierList
from popit.views.misc import GenericOtherNameDetail
from popit.views.misc import GenericOtherNameLinkDetail
from popit.views.misc import GenericOtherNameLinkList
from popit.views.misc import GenericOtherNameList
from popit.views.misc import GenericLinkDetail
from popit.views.misc import GenericLinkList


# Create your views here.
class PersonList(APIView):

    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def get(self, request, language, format=None):
        persons = Person.objects.untranslated().all()
        serializer = PersonSerializer(persons, many=True, language=language)
        return Response(serializer.data)

    def post(self, request, language, format=None):
        serializer = PersonSerializer(data=request.data, language=language)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonDetail(APIView):

    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def get_object(self, pk, language):
        try:
            return Person.objects.language(language).get(id=pk)
        except Person.DoesNotExist:
            return Http404

    def get(self, request, language, pk, format=None):
        person = self.get_object(pk, language)

        serializer = PersonSerializer(person, language=language)
        return Response(serializer.data)

    def put(self, request, language, pk, format=None):
        person = self.get_object(pk, language)
        serializer = PersonSerializer(person, data=request.data, language=language, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, language, pk, format=None):
        person = self.get_object(pk, language)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PersonContactList(GenericContactList):
    serializer = ContactSerializer
    parent = Person


class PersonContactDetail(GenericContactDetail):
    serializer = ContactSerializer
    parent = Person


class PersonOtherNameList(GenericOtherNameList):

    serializer = OtherNameSerializer
    parent = Person


class PersonOtherNameDetail(GenericOtherNameDetail):

    serializer = OtherNameSerializer
    parent = Person


class PersonIdentifierList(GenericIdentifierList):

    serializer = IdentifierSerializer
    parent = Person


class PersonIdentifierDetail(GenericIdentifierDetail):

    serializer = IdentifierSerializer
    parent = Person


class PersonLinkList(GenericLinkList):

    serializer = LinkSerializer
    parent = Person


class PersonLinkDetail(GenericLinkDetail):

    serializer = LinkSerializer
    parent = Person


class PersonContactLinkList(GenericContactLinkList):

    parent = Person
    child = Contact


class PersonContactLinkDetail(GenericContactLinkDetail):
    parent = Person
    child = Contact

    def get_child(self, parent, pk, language):
        if not self.child:
            raise ChildNotSetException("Need to set child object")
        try:
            return parent.contacts.language(language).get(id=pk)
        except self.child.DoesNotExist:
            return Http404


class PersonIdentifierLinkList(GenericIdentifierLinkList):
    parent = Person
    child = Identifier


class PersonIdentifierLinkDetail(GenericIdentifierLinkDetail):
    parent = Person
    child = Identifier


class PersonOtherNameLinkList(GenericOtherNameLinkList):
    parent = Person
    child = OtherName


class PersonOtherNameLinkDetail(GenericOtherNameLinkDetail):
    parent = Person
    child = OtherName
