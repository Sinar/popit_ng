__author__ = 'sweemeng'
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import Http404
from popit.serializers import LinkSerializer
from popit.serializers import ContactDetailSerializer
from popit.serializers import IdentifierSerializer
from popit.serializers import OtherNameSerializer
from popit.serializers import AreaSerializer
from popit.serializers.exceptions import ContentObjectNotAvailable
from popit.serializers.exceptions import SerializerNotSetException
from popit.serializers.exceptions import ParentNotSetException
from popit.serializers.exceptions import ChildNotSetException
from popit.models import Person
from popit.models import ContactDetail
from popit.models import Link
from popit.models import OtherName
from popit.models import Identifier
from popit.models import Area
from popit.views.base import BasePopitView

# TODO: Actually we can just use getattr to access the child objects. But we need to map of attributes :-/

class GenericParentChildList(BasePopitView):

    serializer = None
    parent = None
    # Used with getattr to write less code
    # getattr(parent, child).language(language).get(id=id).
    child_name = None
    child = None


    def get_query(self, parent_pk, language=None):
        parent = self.get_parent(parent_pk, language)
        if language:

            child = getattr(parent, self.child_name).language(language).all()
        else:
            child = getattr(parent, self.child_name).untranslated().all()
        return child

    def get_parent(self, parent_pk, language=None):
        if not self.parent:
            raise ParentNotSetException("No parent object set")
        try:
            if language:
                return self.parent.objects.language(language).get(id=parent_pk)
            else:
                return self.parent.objects.untranslated().get(id=parent_pk)
        except Person.DoesNotExist:
            raise Http404

    def get(self, request, language, parent_pk, format=None):
        if not self.serializer:
            raise SerializerNotSetException("Not Serializer Set")
        obj = self.get_query(parent_pk, language)
        page = self.paginator.paginate_queryset(obj, request, view=self)
        serializer = self.serializer(page, many=True, language=language)

        return self.paginator.get_paginated_response(serializer.data)

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
                data = { "result": serializer.data}
                return Response(data, status.HTTP_201_CREATED)
            except ContentObjectNotAvailable as e:
                return Response({"error": e.message}, status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class GenericContactDetailList(GenericParentChildList):

    serializer = ContactDetailSerializer
    child_name = "contact_details"
    child = ContactDetail


class GenericOtherNameList(GenericParentChildList):

    serializer = OtherNameSerializer
    child_name = "other_names"
    child = OtherName


class GenericIdentifierList(GenericParentChildList):

    serializer = IdentifierSerializer
    child_name = "identifiers"
    child = Identifier


class GenericLinkList(GenericParentChildList):

    serializer = LinkSerializer
    child_name = "links"
    child = Link


class GenericParentChildDetail(BasePopitView):

    serializer = None
    parent = None
    child_name = None
    child = None

    def get_object(self, parent, pk, language=None):
        try:
            if language:
                return getattr(parent, self.child_name).language(language).get(id=pk)
            return getattr(parent, self.child_name).untranslated().get(id=pk)
        except self.child.DoesNotExist:
            raise Http404

    def get_parent(self, parent_pk, language=None):
        if not self.parent:
            raise ParentNotSetException("Parent Not Set")

        try:
            return self.parent.objects.language(language).get(id=parent_pk)
        except Person.DoesNotExist:
            raise Http404

    def get(self, request, language, parent_pk, pk, format=None):
        if not self.serializer:
            raise SerializerNotSetException("No serialization set")
        parent = self.get_parent(parent_pk, language)
        obj = self.get_object(parent, pk)
        serializer = self.serializer(obj, language=language)
        data = { "result": serializer.data }
        return Response(data)

    def put(self, request, language, parent_pk, pk, format=None):
        if not self.serializer:
            raise SerializerNotSetException("No serialization set")

        parent = self.get_parent(parent_pk, language)
        obj = self.get_object(parent, pk)
        if language in obj.get_available_languages():
            obj = self.get_object(parent, pk, language)
        serializer = self.serializer(obj, data=request.data, partial=True, language=language)
        if serializer.is_valid():
            # We do not override where a link is point to.
            serializer.save()
            data = { "result": serializer.data }
            return Response(data, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, language, parent_pk, pk, format=None):
        if not self.serializer:
            raise SerializerNotSetException("No serialization set")
        parent = self.get_parent(parent_pk, language)
        obj = self.get_object(parent, pk)
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Yeah because popolo spec use contact_details, sorry
class GenericContactDetailDetail(GenericParentChildDetail):

    serializer = ContactDetailSerializer
    child_name = "contact_details"
    child = ContactDetail


class GenericOtherNameDetail(GenericParentChildDetail):

    serializer = OtherNameSerializer
    child_name = "other_names"
    child = OtherName


class GenericIdentifierDetail(GenericParentChildDetail):

    serializer = IdentifierSerializer
    child_name = "identifiers"
    child = Identifier


class GenericLinkDetail(GenericParentChildDetail):

    serializer = LinkSerializer
    child_name = "links"
    child = Link


class GenericParentChildLinkList(BasePopitView):

    serializer = LinkSerializer
    parent = None
    child = None
    child_name = None

    def get_parent(self, parent_pk, language):
        if not self.parent:
            raise ParentNotSetException("Parent not set")
        try:
            return self.parent.objects.language(language).get(id=parent_pk)
        except self.parent.DoesNotExist:
            raise Http404

    def get_child(self, parent, pk, language=None):
        if not self.child:
            raise ChildNotSetException("Need to set child object")
        if not self.child_name:
            raise ChildNotSetException("Need to set child name")

        try:
            if language:
                return getattr(parent, self.child_name).language(language).get(id=pk)
            return getattr(parent, self.child_name).untranslated().get(id=pk)

        except self.child.DoesNotExist:
            raise Http404

    def get(self, request, language, parent_pk, pk, format=None):
        parent = self.get_parent(parent_pk, language)
        child = self.get_child(parent, pk, language)
        links = child.links.untranslated().all()
        page = self.paginator.paginate_queryset(links, request, view=self)

        serializer = self.serializer(page, many=True, language=language)
        return self.paginator.get_paginated_response(serializer.data)

    def post(self, request, language, parent_pk, pk, format=None):
        parent = self.get_parent(parent_pk, language)
        child = self.get_child(parent, pk, language)
        serializer = self.serializer(data=request.data, language=language)
        if serializer.is_valid():
            try:
                serializer.save(content_object=child)
                data = { "results": serializer.data }
                return Response(data, status=status.HTTP_201_CREATED)
            except ContentObjectNotAvailable as e:
                # Mostly for idiot that forget to set content object
                return Response({"message": e.message}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GenericContactDetailLinkList(GenericParentChildLinkList):

    child = ContactDetail
    child_name = "contact_details"


class GenericIdentifierLinkList(GenericParentChildLinkList):

    child = Identifier
    child_name = "identifiers"


class GenericOtherNameLinkList(GenericParentChildLinkList):

    child = OtherName
    child_name = "other_names"


class GenericParentChildLinkDetail(BasePopitView):

    serializer = LinkSerializer
    parent = None
    child = None
    child_name = None

    def get_parent(self, parent_pk, language):
        if not self.parent:
            raise ParentNotSetException("Parent not set")
        try:
            return self.parent.objects.language(language).get(id=parent_pk)
        except self.parent.DoesNotExist:
            raise Http404

    def get_child(self, parent, pk, language=None):
        if not self.child:
            raise ChildNotSetException("Need to set child object")
        if not self.child_name:
            raise ChildNotSetException("Need to set child name")
        try:
            if language:
                return getattr(parent, self.child_name).language(language).get(id=pk)
            return getattr(parent, self.child_name).untranslated().get(id=pk)
        except self.child.DoesNotExist:
            raise Http404

    def get(self, request, language, parent_pk, pk, link_pk, format=None):
        parent = self.get_parent(parent_pk, language)
        child = self.get_child(parent, pk, language)
        try:
            link = child.links.language(language).get(id=link_pk)
        except Link.DoesNotExist:
            raise Http404
        serializer = self.serializer(link, language=language)
        data = { "results": serializer.data }
        return Response(data)

    def put(self, request, language, parent_pk, pk, link_pk, format=None):
        parent = self.get_parent(parent_pk, language)
        child = self.get_child(parent, pk, language)
        try:
            link = child.links.language(language).get(id=link_pk)
        except Link.DoesNotExist:
            raise Http404
        serializer = self.serializer(link, data=request.data, partial=True, language=language)
        if serializer.is_valid():
            serializer.save()
            data = { "results": serializer.data }
            return Response(data, status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, language, parent_pk, pk, link_pk, format=None):
        parent = self.get_parent(parent_pk, language)
        child = self.get_child(parent, pk, language)
        try:
            link = child.links.language(language).get(id=link_pk)
        except Link.DoesNotExist:
            raise Http404
        link.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenericContactDetailLinkDetail(GenericParentChildLinkDetail):

    child = ContactDetail
    child_name = "contact_details"


class GenericIdentifierLinkDetail(GenericParentChildLinkDetail):

    child = Identifier
    child_name = "identifiers"


class GenericOtherNameLinkDetail(GenericParentChildLinkDetail):

    child = OtherName
    child_name = "other_names"


class AreaList(BasePopitView):

    def get(self, request, language, format=None):
        areas = Area.objects.untranslated().all()
        page = self.paginator.paginate_queryset(areas, request, view=self)
        serializer = AreaSerializer(page, language=language, many=True)

        return self.paginator.get_paginated_response(serializer.data)

    def post(self, request, language, format=None):
        serializer = AreaSerializer(data=request.data, language=language)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def get_serializer_class(self):
        return AreaSerializer



class AreaDetail(APIView):
    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def get_object(self, pk):
        try:
            return Area.objects.untranslated().get(id=pk)
        except Area.DoesNotExist:
            raise Http404

    def get(self, request, language, pk, format=None):
        area = self.get_object(pk)
        serializer = AreaSerializer(area, language=language)
        data = { "results": serializer.data }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, language, pk, format=None):
        area = self.get_object(pk)
        serializer = AreaSerializer(area, data=request.data, language=language, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = { "results": serializer.data }
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, language, pk, format=None):
        area = self.get_object(pk)
        area.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
       
    def get_serializer_class(self):
        return AreaSerializer



class AreaLinkList(GenericLinkList):
    parent = Area


class AreaLinkDetail(GenericLinkDetail):
    parent = Area
