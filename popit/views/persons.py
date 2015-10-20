__author__ = 'sweemeng'
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import Http404
from popit.serializers import PersonSerializer
from popit.models import Person


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

