__author__ = 'sweemeng'
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import Http404
from popit.serializers import PersonSerializer
from popit.models import Person
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
            raise Http404

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
    parent = Person


class PersonContactDetail(GenericContactDetail):
    parent = Person


class PersonOtherNameList(GenericOtherNameList):
    parent = Person


class PersonOtherNameDetail(GenericOtherNameDetail):
    parent = Person


class PersonIdentifierList(GenericIdentifierList):
    parent = Person


class PersonIdentifierDetail(GenericIdentifierDetail):
    parent = Person


class PersonLinkList(GenericLinkList):
    parent = Person


class PersonLinkDetail(GenericLinkDetail):
    parent = Person


class PersonContactLinkList(GenericContactLinkList):
    parent = Person


class PersonContactLinkDetail(GenericContactLinkDetail):
    parent = Person


class PersonIdentifierLinkList(GenericIdentifierLinkList):
    parent = Person


class PersonIdentifierLinkDetail(GenericIdentifierLinkDetail):
    parent = Person


class PersonOtherNameLinkList(GenericOtherNameLinkList):
    parent = Person


class PersonOtherNameLinkDetail(GenericOtherNameLinkDetail):
    parent = Person
