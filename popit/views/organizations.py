__author__ = 'sweemeng'
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import Http404
from popit.serializers import OrganizationSerializer
from popit.models import Organization
from popit.views.misc import GenericContactDetailDetail
from popit.views.misc import GenericContactDetailLinkDetail
from popit.views.misc import GenericContactDetailLinkList
from popit.views.misc import GenericContactDetailList
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
from popit.views.base import BasePopitDetailUpdateView
from popit.views.base import BasePopitListCreateView
from popit.views.citation import BaseCitationDetailView
from popit.views.citation import BaseCitationListCreateView
from popit.views.citation import GenericContactDetailCitationListView
from popit.views.citation import GenericContactDetailCitationDetailView
from popit.views.citation import GenericOthernameCitationListView
from popit.views.citation import GenericOthernameCitationDetailView
from popit.views.citation import GenericIdentifierCitationListView
from popit.views.citation import GenericIdentifierCitationDetailView
from popit.views.citation import BaseFieldCitationView
from popit.views.citation import GenericContactDetailFieldCitationView
from popit.views.citation import GenericIdentifierFieldCitationView
from popit.views.citation import GenericOtherNameFieldCitationView


class OrganizationList(BasePopitListCreateView):

    entity = Organization
    serializer = OrganizationSerializer


class OrganizationDetail(BasePopitDetailUpdateView):

    entity = Organization
    serializer = OrganizationSerializer


# This might be able to make into the constructor
# If can't, then we should make a factory for this :-/
class OrganizationContactDetailList(GenericContactDetailList):
    parent = Organization


class OrganizationContactDetailDetail(GenericContactDetailDetail):
    parent = Organization


class OrganizationContactDetailLinkList(GenericContactDetailLinkList):
    parent = Organization


class OrganizationContactDetailLinkDetail(GenericContactDetailLinkDetail):
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



class OrganizationCitationListCreateView(BaseCitationListCreateView):
    entity = Organization


class OrganizationCitationDetailView(BaseCitationDetailView):
    entity = Organization


class OrganizationContactDetailCitationListView(GenericContactDetailCitationListView):
    parent = Organization


class OrganizationContactDetailCitationDetailView(GenericContactDetailCitationDetailView):
    parent = Organization


class OrganizationIdentifierCitationListView(GenericIdentifierCitationListView):
    parent = Organization


class OrganizationIdentifierCitationDetailView(GenericIdentifierCitationDetailView):
    parent = Organization


class OrganizationOthernameCitationListView(GenericOthernameCitationListView):
    parent = Organization


class OrganizationOthernameCitationDetailView(GenericOthernameCitationDetailView):
    parent = Organization


class OrganizationFieldCitationView(BaseFieldCitationView):
    entity = Organization


class OrganizationContactDetailFieldCitationView(GenericContactDetailFieldCitationView):
    parent = Organization


class OrganizationIdentifierFieldCitationView(GenericIdentifierFieldCitationView):
    parent = Organization


class OrganizationOtherNameFieldCitationView(GenericOtherNameFieldCitationView):
    parent = Organization