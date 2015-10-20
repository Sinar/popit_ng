__author__ = 'sweemeng'
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import Http404
from popit.serializers import LinkSerializer
from popit.serializers.exceptions import ContentObjectNotAvailable
from popit.serializers.exceptions import SerializerNotSetException
from popit.serializers.exceptions import ParentNotSetException
from popit.serializers.exceptions import ChildNotSetException
from popit.models import Person
from popit.models import Contact


class GenericParentChildList(APIView):
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    serializer = None
    parent = None

    def get_query(self, parent_pk, language):
        raise NotImplementedError()

    def get_parent(self, parent_pk, language):
        if not self.parent:
            raise ParentNotSetException("No parent object set")
        try:
            return self.parent.objects.language(language).get(id=parent_pk)
        except Person.DoesNotExist:
            return Http404

    def get(self, request, language, parent_pk, format=None):
        if not self.serializer:
            raise SerializerNotSetException("Not Serializer Set")
        obj = self.get_query(parent_pk, language)
        serializer = self.serializer(obj, many=True, language=language)

        return Response(serializer.data)

    def post(self, request, language, parent_pk, format=None):
        if not self.serializer:
            raise SerializerNotSetException("No serializer set")
        if not self.parent:
            raise ParentNotSetException("No parent set")
        parent = self.get_parent(parent_pk, language)

        serializer = self.serializer(data=request.data, language=language)
        if serializer.is_valid():
            try:
                serializer.save(content_object=parent)
                return Response(serializer.data, status.HTTP_201_CREATED)
            except ContentObjectNotAvailable as e:
                return Response({"error": e.message}, status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class GenericContactList(GenericParentChildList):
    def get_query(self, parent_pk, language):
        parent = self.get_parent(parent_pk, language)

        contacts = parent.contacts.untranslated().all()
        return contacts


class GenericOtherNameList(GenericParentChildList):
    def get_query(self, parent_pk, language):
        parent = self.get_parent(parent_pk, language)

        other_names = parent.other_names.untranslated().all()
        return other_names


class GenericIdentifierList(GenericParentChildList):
    def get_query(self, parent_pk, language):
        parent = self.get_parent(parent_pk, language)

        identifiers = parent.identifiers.untranslated().all()
        return identifiers


class GenericLinkList(GenericParentChildList):
    def get_query(self, parent_pk, language):
        parent = self.get_parent(parent_pk, language)

        links = parent.links.untranslated().all()
        return links


class GenericParentChildDetail(APIView):

    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    serializer = None
    parent = None

    def get_object(self, parent, pk):
        raise NotImplementedError()

    def get_parent(self, parent_pk, language):
        if not self.parent:
            raise ParentNotSetException("Parent Not Set")

        try:
            return self.parent.objects.language(language).get(id=parent_pk)
        except Person.DoesNotExist:
            return Http404

    def get(self, request, language, parent_pk, pk, format=None):
        if not self.serializer:
            raise SerializerNotSetException("No serialization set")
        parent = self.get_parent(parent_pk, language)
        obj = self.get_object(parent, pk)
        serializer = self.serializer(obj, language=language)
        return Response(serializer.data)

    def put(self, request, language, parent_pk, pk, format=None):
        if not self.serializer:
            raise SerializerNotSetException("No serialization set")

        parent = self.get_parent(parent_pk, language)
        obj = self.get_object(parent, pk)
        serializer = self.serializer(obj, data=request.data, partial=True)
        if serializer.is_valid():
            # We do not override where a link is point to.
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, language, parent_pk, pk, format=None):
        if not self.serializer:
            raise SerializerNotSetException("No serialization set")
        parent = self.get_parent(parent_pk, language)
        obj = self.get_object(parent, pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenericContactDetail(GenericParentChildDetail):
    def get_object(self, parent, pk):
        try:
            return parent.contacts.untranslated().get(id=pk)
        except Contact.DoesNotExist:
            return Http404


class GenericOtherNameDetail(GenericParentChildDetail):
    def get_object(self, parent, pk):
        try:
            return parent.other_names.untranslated().get(id=pk)
        except Contact.DoesNotExist:
            return Http404


class GenericIdentifierDetail(GenericParentChildDetail):

    def get_object(self, parent, pk):
        try:
            return parent.identifiers.untranslated().get(id=pk)
        except Contact.DoesNotExist:
            return Http404


class GenericLinkDetail(GenericParentChildDetail):
    def get_object(self, parent, pk):
        try:
            return parent.links.untranslated().get(id=pk)
        except Contact.DoesNotExist:
            return Http404


class GenericParentChildLinkList(APIView):

    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    serializer = LinkSerializer
    parent = None
    child = None

    def get_parent(self, parent_pk, language):
        if not self.parent:
            raise ParentNotSetException("Parent not set")
        try:
            return self.parent.objects.language(language).get(id=parent_pk)
        except self.parent.DoesNotExist:
            return Http404

    def get_child(self, parent, pk, language):
        raise NotImplementedError()

    def get(self, request, language, parent_pk, pk):
        parent = self.get_parent(parent_pk, language)
        child = self.get_child(parent, pk, language)
        links = child.links.untranslated().all()
        serializer = self.serializer(links, many=True, language=language)
        return Response(serializer.data)

    def post(self, request, language, parent_pk, pk):
        parent = self.get_parent(parent_pk, language)
        child = self.get_child(parent, pk, language)
        serializer = self.serializer(data=request.data, language=language)
        if serializer.is_valid():
            try:
                serializer.save(content_object=child)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ContentObjectNotAvailable as e:
                # Mostly for idiot that forget to set content object
                return Response({"message": e.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GenericContactLinkList(GenericParentChildLinkList):
    def get_child(self, parent, pk, language):
        if not self.child:
            raise ChildNotSetException("Need to set child object")
        try:
            return parent.contacts.language(language).get(id=pk)
        except self.child.DoesNotExist:
            return Http404


class GenericIdentifierLinkList(GenericParentChildLinkList):
    def get_child(self, parent, pk, language):
        if not self.child:
            raise ChildNotSetException("Need to set child object")
        try:
            return parent.identifiers.language(language).get(id=pk)
        except self.child.DoesNotExist:
            return Http404


class GenericOtherNameLinkList(GenericParentChildLinkList):
    def get_child(self, parent, pk, language):
        if not self.child:
            raise ChildNotSetException("Need to set child object")
        try:
            return parent.other_names.language(language).get(id=pk)
        except self.child.DoesNotExist:
            return Http404


class GenericParentChildLinkDetail(APIView):

    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    serializer = LinkSerializer
    parent = None
    child = None

    def get_parent(self, parent_pk, language):
        if not self.parent:
            raise ParentNotSetException("Parent not set")
        try:
            return self.parent.objects.language(language).get(id=parent_pk)
        except self.parent.DoesNotExist:
            return Http404

    def get_child(self, parent, pk, language):
        raise NotImplementedError()

    def get(self, request, language, parent_pk, pk, link_pk):
        parent = self.get_parent(parent_pk, language)
        child = self.get_child(parent, pk, language)
        link = child.links.language(language).get(id=link_pk)
        serializer = self.serializer(link, language=language)
        return Response(serializer.data)

    def put(self, request, language, parent_pk, pk, link_pk):
        parent = self.get_parent(parent_pk, language)
        child = self.get_child(parent, pk, language)
        link = child.links.language(language).get(id=link_pk)
        serializer = self.serializer(link, data=request.data, partial=True, language=language)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, language, parent_pk, pk, link_pk):
        parent = self.get_parent(parent_pk, language)
        child = self.get_child(parent, pk, language)
        link = child.links.language(language).get(id=link_pk)
        link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenericContactLinkDetail(GenericParentChildLinkDetail):
    def get_child(self, parent, pk, language):
        if not self.child:
            raise ChildNotSetException("Need to set child object")
        try:
            return parent.contacts.language(language).get(id=pk)
        except self.child.DoesNotExist:
            return Http404


class GenericIdentifierLinkDetail(GenericParentChildLinkDetail):
    def get_child(self, parent, pk, language):
        if not self.child:
            raise ChildNotSetException("Need to set child object")
        try:
            return parent.identifiers.language(language).get(id=pk)
        except self.child.DoesNotExist:
            return Http404


class GenericOtherNameLinkDetail(GenericParentChildLinkDetail):
    def get_child(self, parent, pk, language):
        if not self.child:
            raise ChildNotSetException("Need to set child object")
        try:
            return parent.other_names.language(language).get(id=pk)
        except self.child.DoesNotExist:
            return Http404