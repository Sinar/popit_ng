from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.settings import api_settings
from rest_framework.response import Response
from django.http import Http404
from popit.models import Person
from popit.serializers import PersonSerializer
from rest_framework import status
from popit.views.exception import SerializerNotSetException
from popit.views.exception import EntityNotSetException


# Maybe we should extract this to a general view to be used by others
class BasePopitView(APIView):

    paginator_class = api_settings.DEFAULT_PAGINATION_CLASS

    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    _paginator = None

    entity = None
    serializer = None

    @property
    def paginator(self):
        if not self._paginator:
            self._paginator = self.paginator_class()
        return self._paginator


class BasePopitListCreateView(BasePopitView):

    def get(self, request, language, format=True):
        if not self.serializer:
            raise SerializerNotSetException("Need to set serializer in class")

        if not self.entity:
            raise EntityNotSetException("Please set an entity in views")

        entities = self.entity.objects.untranslated().all()
        page = self.paginator.paginate_queryset(entities, request, view=self)
        serializer = self.serializer(page, language=language, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def post(self, request, language, format=True):
        if not self.serializer:
            raise SerializerNotSetException("Need to set serializer in class")

        if not self.entity:
            raise EntityNotSetException("Please set an entity in views")

        serializer = self.serializer(data=request.data, language=language)
        if serializer.is_valid():
            serializer.save()
            data = { "result": serializer.data }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BasePopitDetailUpdateView(BasePopitView):
    def get_object(self, pk):
        if not self.entity:
            raise EntityNotSetException("Please sent entity in class")

        if not self.serializer:
            raise SerializerNotSetException("Please set serializer in class")

        try:
            return self.entity.objects.untranslated().get(id=pk)
        except self.entity.DoesNotExist:
            raise Http404

    def get(self, request, language, pk, format=True):
        instance = self.get_object(pk)

        serializer = self.serializer(instance, language=language)
        data = { "result": serializer.data }
        return Response(data)

    def put(self, request, language, pk, format=True):
        instance = self.get_object(pk)
        serializer = self.serializer(instance, data=request.data, language=language, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = { "result": serializer.data }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, language, pk, format=True):
        instance = self.get_object(pk)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)