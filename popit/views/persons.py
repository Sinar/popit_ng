__author__ = 'sweemeng'
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import Http404
from popit.serializers import PersonSerializer
from popit.models import Person
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
from popit.views.base import BasePopitListCreateView
from popit.views.base import BasePopitDetailUpdateView
from popit.views.citation import BaseCitationDetailView
from popit.views.citation import BaseCitationListCreateView
from popit.views.citation import BaseSubItemCitationListView
from popit.views.citation import BaseSubItemCitationDetailView
from popit.views.citation import GenericOthernameCitationListView
from popit.views.citation import GenericOthernameCitationDetailView
from popit.views.citation import GenericIdentifierCitationListView
from popit.views.citation import GenericIdentifierCitationDetailView
from popit.views.citation import GenericContactDetailCitationListView
from popit.views.citation import GenericContactDetailCitationDetailView
from popit.views.citation import BaseFieldCitationView
from popit.views.citation import GenericOtherNameFieldCitationView
from popit.views.citation import GenericIdentifierFieldCitationView
from popit.views.citation import GenericContactDetailFieldCitationView


# Create your views here.
class PersonList(BasePopitListCreateView):
    entity = Person
    serializer = PersonSerializer


class PersonDetail(BasePopitDetailUpdateView):
    entity = Person
    serializer = PersonSerializer


class PersonContactDetailList(GenericContactDetailList):
    parent = Person


class PersonContactDetailDetail(GenericContactDetailDetail):
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


class PersonContactDetailLinkList(GenericContactDetailLinkList):
    parent = Person


class PersonContactDetailLinkDetail(GenericContactDetailLinkDetail):
    parent = Person


class PersonIdentifierLinkList(GenericIdentifierLinkList):
    parent = Person


class PersonIdentifierLinkDetail(GenericIdentifierLinkDetail):
    parent = Person


class PersonOtherNameLinkList(GenericOtherNameLinkList):
    parent = Person


class PersonOtherNameLinkDetail(GenericOtherNameLinkDetail):
    parent = Person


class PersonCitationListCreateView(BaseCitationListCreateView):
    entity = Person


class PersonCitationDetailView(BaseCitationDetailView):
    entity = Person


class PersonOthernameCitationListView(GenericOthernameCitationListView):
    parent = Person


class PersonOthernameCitationDetailView(GenericOthernameCitationDetailView):
    parent = Person


class PersonContactDetailCitationListView(GenericContactDetailCitationListView):
    parent = Person


class PersonContactDetailCitationDetailView(GenericContactDetailCitationDetailView):
    parent = Person


class PersonIdentifierCitationListView(GenericIdentifierCitationListView):
    parent = Person


class PersonIdentifierCitationDetailView(GenericIdentifierCitationDetailView):
    parent = Person


class PersonFieldCitationView(BaseFieldCitationView):
    entity = Person


class PersonOtherNameFieldCitationView(GenericOtherNameFieldCitationView):
    entity = Person


class PersonIdentifierFieldCitationView(GenericIdentifierFieldCitationView):
    entity = Person


class PersonContactDetailFieldCitationView(GenericContactDetailFieldCitationView):
    entity = Person
