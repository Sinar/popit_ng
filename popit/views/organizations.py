__author__ = 'sweemeng'
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import Http404
from popit.serializers import OrganizationSerializer
from popit.models import Organization
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


class OrganizationList(APIView):

    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def get(self, request, language, format=None):
        organizations = Organization.objects.untranslated().all()
        serializer = OrganizationSerializer(organizations, many=True, language=language)
        return Response(serializer.data)

    def post(self, request, language, format=None):
        serializer = OrganizationSerializer(data=request.data, language=language)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrganizationDetail(APIView):

    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def get_object(self, pk):
        try:
            return Organization.objects.untranslated().get(id=pk)
        except Organization.DoesNotExist:
            return Http404

    def get(self, request, language, pk, format=None):
        organization = self.get_object(pk)
        serializer = OrganizationSerializer(organization, language=language)
        return Response(serializer.data)

    def put(self, request, language, pk, format=None):
        organization = self.get_object(pk)
        serializer = OrganizationSerializer(organization, data=request.data, language=language, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, language, pk, format=None):
        organization = self.get_object(pk)
        organization.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# This might be able to make into the constructor
# If can't, then we should make a factory for this :-/
class OrganizationContactList(GenericContactList):
    parent = Organization


class OrganizationContactDetail(GenericContactDetail):
    parent = Organization


class OrganizationContactLinkList(GenericContactLinkList):
    parent = Organization


class OrganizationContactLinkDetail(GenericContactLinkDetail):
    parent = Organization


class OrganizationIdentifierList(GenericIdentifierList):
    parent = Organization


class OrganizationIdentifierDetail(GenericIdentifierDetail):
    parent = Organization


class OrganizationIdentifierLinkList(GenericIdentifierLinkList):
    parent = Organization


class OrganizationIdentifierLinkDetail(GenericIdentifierLinkDetail):
    parent = Organization


class OrganizationOtherNameList(GenericOtherNameList):
    parent = Organization


class OrganizationOtherNameDetail(GenericOtherNameDetail):
    parent = Organization


class OrganizationOtherNameLinkList(GenericOtherNameLinkList):
    parent = Organization


class OrganizationOtherNameLinkDetail(GenericOtherNameLinkDetail):
    parent = Organization


class OrganizationLinkList(GenericLinkList):
    parent = Organization


class OrganizationLinkDetail(GenericLinkDetail):
    parent = Organization