from popit.views.base import BasePopitView
from popit.serializers import LinkSerializer
from popit.models import Link
from popit.models import Person
from popit.models import Organization
from popit.models import Post
from popit.models import Membership
from popit.models import OtherName
from popit.models import Identifier
from popit.models import ContactDetail
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
from popit.serializers.exceptions import ParentNotSetException
from popit.serializers.exceptions import ChildNotSetException
from popit.serializers.exceptions import ContentObjectNotAvailable


# Why citation refers to a field, not a link
class BaseCitationListCreateView(BasePopitView):

    serializer = LinkSerializer

    def get(self, request, language, pk, field):
        instance = self.entity.objects.language(language).get(id=pk)
        citations = instance.links.untranslated().filter(field=field)
        page = self.paginator.paginate_queryset(citations, request, view=self)

        serializer = self.serializer(page, language=language, many=True)

        return self.paginator.get_paginated_response(serializer.data)

    def post(self, request, language, pk, field):
        instance = self.entity.objects.language(language).get(id=pk)

        # Just add if not there, it is implied that field is based on url. Override if added
        data = request.data
        data["field"] = field

        serializer = self.serializer(data=data, language=language)
        if serializer.is_valid():
            serializer.save(content_object=instance)
            output = {
                "result": serializer.data
            }
            return Response(output, status=status.HTTP_201_CREATED)
        errors = {"errors": serializer.errors}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class BaseCitationDetailView(BasePopitView):

    serializer = LinkSerializer

    def get_object(self, parent, field, pk, language="en"):
        try:
            instance = self.entity.objects.language(language).get(id=parent)
            try:
                citations = instance.links.get(id=pk, field=field)
            except Link.DoesNotExist:
                raise Http404
            return citations

        except self.entity.DoesNotExist:
            raise Http404

    def get(self, request, language, parent, field, pk):
        citations = self.get_object(parent, field, pk, language)
        serializer = self.serializer(instance=citations, language=language)
        data = {"result": serializer.data}
        return Response(data)

    def put(self, request, language, parent, field, pk):
        citations = self.get_object(parent, field, pk, language)
        serializer = self.serializer(citations, data=request.data, language=language)
        if serializer.is_valid():
            serializer.save()
            output = {"result":serializer.data}
            return Response(output, status=status.HTTP_200_OK)
        errors = {"errors":serializer.errors}
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, language, parent, field, pk):
        citations = self.get_object(parent, field, pk, language)
        citations.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BaseSubItemCitationListView(BasePopitView):

    serializer = LinkSerializer
    parent = None

    def get_parent(self, parent_pk, language):
        try:
            parent = self.parent.objects.language(language).get(id=parent_pk)
            return parent
        except self.parent.DoesNotExist:
            raise Http404

    def get_citations(self, parent_pk, child_pk, field, language):
        try:
            parent = self.get_parent(parent_pk ,language)
            child = self.get_child(parent, child_pk, language)
            links = child.links.language(language).filter(field=field)
            return links
        except Link.DoesNotExist:
            raise Http404

    def get_child(self, parent, child_pk, language):
        raise NotImplemented

    def get(self, request, language, parent_pk, child_pk, field):
        citations = self.get_citations(parent_pk, child_pk, field, language)
        page = self.paginator.paginate_queryset(citations, request, view=self)
        serializer = self.serializer(page, language=language, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    def post(self, request, language, parent_pk, child_pk, field):
        parent = self.get_parent(parent_pk, language)
        child = self.get_child(parent, child_pk, language)
        serializer = self.serializer(data=request.data, language=language)
        if serializer.is_valid():
            serializer.save(content_object=child)
            data = { "result": serializer.data }
            return Response(data, status=status.HTTP_201_CREATED)

        errors = { "errors": serializer.errors }
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)


class GenericOthernameCitationListView(BaseSubItemCitationListView):
    entity = OtherName

    def get_child(self, parent, child_pk, language):
        try:
            child = parent.other_names.language(language).get(id=child_pk)
            return child
        except self.entity.DoesNotExist:
            raise Http404


class GenericIdentifierCitationListView(BaseSubItemCitationListView):
    entity = Identifier

    def get_child(self, parent, child_pk, language):
        try:
            child = parent.identifiers.language(language).get(id=child_pk)
            return child
        except self.entity.DoesNotExist:
            raise Http404


class GenericContactDetailCitationListView(BaseSubItemCitationListView):
    entity = ContactDetail

    def get_child(self, parent, child_pk, language):
        try:
            child = parent.contact_details.language(language).get(id=child_pk)
            return child
        except self.entity.DoesNotExist:
            raise Http404


class BaseSubItemCitationDetailView(BasePopitView):
    serializer = LinkSerializer
    parent = None

    def get_parent(self, parent_pk, language):
        try:
            parent = self.parent.objects.language(language).get(id=parent_pk)
            return parent
        except self.parent.DoesNotExist:
            raise Http404

    def get_citations(self, parent_pk, child_pk, field, link_id, language):
        try:
            parent = self.get_parent(parent_pk ,language)
            child = self.get_child(parent, child_pk, language)
            links = child.links.language(language).get(id=link_id, field=field)
            return links
        except Link.DoesNotExist:
            raise Http404

    def get_child(self, parent, child_pk, language):
        raise NotImplemented

    def get(self, requests, language, parent_pk, child_pk, field, link_id):
        citations = self.get_citations(parent_pk, child_pk, field, link_id, language)
        serializer = self.serializer(citations, language=language)
        result = { "result": serializer.data }
        return Response(result)

    def put(self, requests, language, parent_pk, child_pk, field, link_id):
        data = requests.data
        citations = self.get_citations(parent_pk, child_pk, field, link_id, language)
        serializer = self.serializer(citations, data=data, language=language)
        if serializer.is_valid():
            serializer.save()
            result = { "result": serializer.data }
            return Response(result, status=status.HTTP_200_OK)
        errors = { "errors": serializer.errors }
        return Response(errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, requests, language, parent_pk, child_pk, field, link_id):
        citations = self.get_citations(parent_pk, child_pk, field, link_id, language)
        citations.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenericOthernameCitationDetailView(BaseSubItemCitationDetailView):
    entity = OtherName

    def get_child(self, parent, child_pk, language):

        try:
            child = parent.other_names.language(language).get(id=child_pk)
            return child
        except self.entity.DoesNotExist:
            raise Http404


class GenericIdentifierCitationDetailView(BaseSubItemCitationDetailView):
    entity = Identifier

    def get_child(self, parent, child_pk, language):
        try:
            child = parent.identifiers.language(language).get(id=child_pk)
            return child
        except self.entity.DoesNotExist:
            raise Http404


class GenericContactDetailCitationDetailView(BaseSubItemCitationDetailView):
    entity = ContactDetail

    def get_child(self, parent, child_pk, language):
        try:
            child = parent.contact_details.language(language).get(id=child_pk)
            return child
        except self.entity.DoesNotExist:
            raise Http404


# This is a view only view to see which field have citations. No create/update/delete
class BaseFieldCitationView(BasePopitView):

    serializer = LinkSerializer

    def get_citations(self, pk, language):
        data = {}
        instance = self.entity.objects.language(language).get(id=pk)
        for field in instance._meta.fields:
            # I don't care about id, and yes it is hardcoded I don't care!
            if field.attname == "id":
                continue
            temp = instance.links.filter(field=field.attname)
            citations = LinkSerializer(temp, language=language, many=True)
            data[field.attname] = citations.data

        # Turns out that in hvad translated field is in another db. Which is cool then we can add more language without alter table!!
        for field in instance._translated_field_names:
            # I don't care about id, and yes it is hardcoded I don't care!
            if field == "master_id" or field == "id":
                continue
            temp = instance.links.filter(field=field)
            citations = LinkSerializer(temp, language=language, many=True)
            data[field] = citations.data
        return data

    def get(self, request, language, pk):
        citations = self.get_citations(pk, language)
        data = {"result": citations}
        return Response(data)


class BaseSubItemFieldCitationView(BasePopitView):

    parent = None
    serializer = LinkSerializer

    def get_parent(self, parent_pk, language):
        try:
            parent = self.parent.objects.language(language).get(id=parent_pk)
            return parent
        except self.parent.DoesNotExist:
            raise Http404

    def get_citations(self, parent_pk, child_pk, language):
        parent = self.get_parent(parent_pk, language)
        child = self.get_child(parent, child_pk, language)
        data = {}
        for field in child._meta.fields:
            if field.attname == "content_object":
                continue
            temp = child.links.filter(field=field.attname)
            citation = LinkSerializer(temp, language=language, many=True)
            data[field.attname] = citation.data
        return data

    def get_child(self, parent, child_pk, language):
        raise NotImplemented

    def get(self, request, language, parent_pk, child_pk):
        citations = self.get_citations(parent_pk, child_pk, language)
        result = { "result": citations }
        return Response(result)


class GenericOtherNameFieldCitationView(BaseSubItemFieldCitationView):
    entity = OtherName

    def get_child(self, parent, child_pk, language):
        try:
            child = parent.other_names.language(language).get(id=child_pk)
            return child
        except self.entity.DoesNotExist:
            raise Http404


class GenericIdentifierFieldCitationView(BaseSubItemFieldCitationView):
    entity = Identifier

    def get_child(self, parent, child_pk, language):
        try:
            child = parent.identifiers.language(language).get(id=child_pk)
            return child
        except self.entity.DoesNotExist:
            raise Http404


class GenericContactDetailFieldCitationView(BaseSubItemFieldCitationView):
    entity = ContactDetail

    def get_child(self, parent, child_pk, language):
        try:
            child = parent.contact_details.language(language).get(id=child_pk)
            return child
        except self.entity.DoesNotExist:
            raise Http404