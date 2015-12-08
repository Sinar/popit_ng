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



class GenericParentChildList(BasePopitView):

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
                data = { "results": serializer.data}
                return Response(data, status.HTTP_201_CREATED)
            except ContentObjectNotAvailable as e:
                return Response({"error": e.message}, status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class GenericContactDetailList(GenericParentChildList):

    serializer = ContactDetailSerializer

    def get_query(self, parent_pk, language):
        parent = self.get_parent(parent_pk, language)

        contact_details = parent.contact_details.untranslated().all()
        return contact_details


class GenericOtherNameList(GenericParentChildList):

    serializer = OtherNameSerializer

    def get_query(self, parent_pk, language):
        parent = self.get_parent(parent_pk, language)

        other_names = parent.other_names.untranslated().all()
        return other_names


class GenericIdentifierList(GenericParentChildList):

    serializer = IdentifierSerializer

    def get_query(self, parent_pk, language):
        parent = self.get_parent(parent_pk, language)

        identifiers = parent.identifiers.untranslated().all()
        return identifiers


class GenericLinkList(GenericParentChildList):

    serializer = LinkSerializer

    def get_query(self, parent_pk, language):
        parent = self.get_parent(parent_pk, language)

        links = parent.links.untranslated().all()
        return links


class GenericParentChildDetail(BasePopitView):

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
            raise Http404

    def get(self, request, language, parent_pk, pk, format=None):
        if not self.serializer:
            raise SerializerNotSetException("No serialization set")
        parent = self.get_parent(parent_pk, language)
        obj = self.get_object(parent, pk)
        serializer = self.serializer(obj, language=language)
        data = { "results": serializer.data }
        return Response(data)

    def put(self, request, language, parent_pk, pk, format=None):
        if not self.serializer:
            raise SerializerNotSetException("No serialization set")

        parent = self.get_parent(parent_pk, language)
        obj = self.get_object(parent, pk)
        serializer = self.serializer(obj, data=request.data, partial=True, language=language)
        if serializer.is_valid():
            # We do not override where a link is point to.
            serializer.save()
            data = { "results": serializer.data }
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

    def get_object(self, parent, pk):
        try:
            return parent.contact_details.untranslated().get(id=pk)
        except ContactDetail.DoesNotExist:
            raise Http404


class GenericOtherNameDetail(GenericParentChildDetail):

    serializer = OtherNameSerializer

    def get_object(self, parent, pk):
        try:
            return parent.other_names.untranslated().get(id=pk)
        except OtherName.DoesNotExist:
            raise Http404


class GenericIdentifierDetail(GenericParentChildDetail):

    serializer = IdentifierSerializer

    def get_object(self, parent, pk):
        try:
            return parent.identifiers.untranslated().get(id=pk)
        except Identifier.DoesNotExist:
            raise Http404


class GenericLinkDetail(GenericParentChildDetail):

    serializer = LinkSerializer

    def get_object(self, parent, pk):
        try:
            return parent.links.untranslated().get(id=pk)
        except Link.DoesNotExist:
            raise Http404


class GenericParentChildLinkList(BasePopitView):

    serializer = LinkSerializer
    parent = None
    child = None

    def get_parent(self, parent_pk, language):
        if not self.parent:
            raise ParentNotSetException("Parent not set")
        try:
            return self.parent.objects.language(language).get(id=parent_pk)
        except self.parent.DoesNotExist:
            raise Http404

    def get_child(self, parent, pk, language):
        raise NotImplementedError()

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

    def get_child(self, parent, pk, language):
        if not self.child:
            raise ChildNotSetException("Need to set child object")
        try:
            return parent.contact_details.language(language).get(id=pk)
        except self.child.DoesNotExist:
            raise Http404


class GenericIdentifierLinkList(GenericParentChildLinkList):

    child = Identifier

    def get_child(self, parent, pk, language):
        if not self.child:
            raise ChildNotSetException("Need to set child object")
        try:
            return parent.identifiers.language(language).get(id=pk)
        except self.child.DoesNotExist:
            raise Http404


class GenericOtherNameLinkList(GenericParentChildLinkList):

    child = OtherName

    def get_child(self, parent, pk, language):
        if not self.child:
            raise ChildNotSetException("Need to set child object")
        try:
            return parent.other_names.language(language).get(id=pk)
        except self.child.DoesNotExist:
            raise Http404


class GenericParentChildLinkDetail(BasePopitView):

    serializer = LinkSerializer
    parent = None
    child = None

    def get_parent(self, parent_pk, language):
        if not self.parent:
            raise ParentNotSetException("Parent not set")
        try:
            return self.parent.objects.language(language).get(id=parent_pk)
        except self.parent.DoesNotExist:
            raise Http404

    def get_child(self, parent, pk, language):
        raise NotImplementedError()

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
            return Response(serializer.data, status.HTTP_200_OK)
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

    def get_child(self, parent, pk, language):
        if not self.child:
            raise ChildNotSetException("Need to set child object")
        try:
            return parent.contact_details.language(language).get(id=pk)
        except self.child.DoesNotExist:
            raise Http404


class GenericIdentifierLinkDetail(GenericParentChildLinkDetail):

    child = Identifier

    def get_child(self, parent, pk, language):
        if not self.child:
            raise ChildNotSetException("Need to set child object")
        try:
            return parent.identifiers.language(language).get(id=pk)
        except self.child.DoesNotExist:
            raise Http404


class GenericOtherNameLinkDetail(GenericParentChildLinkDetail):

    child = OtherName

    def get_child(self, parent, pk, language):
        if not self.child:
            raise ChildNotSetException("Need to set child object")
        try:
            return parent.other_names.language(language).get(id=pk)
        except self.child.DoesNotExist:
            raise Http404


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


class AreaLinkList(GenericLinkList):
    parent = Area


class AreaLinkDetail(GenericLinkDetail):
    parent = Area