from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import Http404
from popit.models import Relation
from popit.views.misc import GenericContactDetailDetail
from popit.views.misc import GenericContactDetailList
from popit.views.misc import GenericContactDetailLinkDetail
from popit.views.misc import GenericContactDetailLinkList
from popit.views.misc import GenericIdentifierDetail
from popit.views.misc import GenericIdentifierLinkDetail
from popit.views.misc import GenericIdentifierLinkList
from popit.views.misc import GenericIdentifierList
from popit.views.misc import GenericLinkDetail
from popit.views.misc import GenericLinkList
from popit.serializers import RelationSerializer
from popit.views.base import BasePopitDetailUpdateView
from popit.views.base import BasePopitListCreateView
from popit.views.citation import BaseCitationDetailView
from popit.views.citation import BaseCitationListCreateView
from popit.views.citation import GenericContactDetailCitationDetailView
from popit.views.citation import GenericContactDetailCitationListView
from popit.views.citation import GenericIdentifierCitationListView
from popit.views.citation import GenericIdentifierCitationDetailView
from popit.views.citation import BaseFieldCitationView
from popit.views.citation import GenericContactDetailFieldCitationView
from popit.views.citation import GenericIdentifierFieldCitationView
from popit.serializers.minimized import MinRelationSerializer


class RelationList(BasePopitListCreateView):
    serializer = RelationSerializer
    mini_serializer = MinRelationSerializer
    entity = Relation


class RelationDetail(BasePopitDetailUpdateView):

    serializer = RelationSerializer
    mini_serializer = MinRelationSerializer
    entity = Relation


class RelationLinkDetail(GenericLinkDetail):
    parent = Relation


class RelationLinkList(GenericLinkList):
    parent = Relation


class RelationIdentifierList(GenericIdentifierList):
    parent = Relation


class RelationIdentifierDetail(GenericIdentifierDetail):
    parent = Relation


class RelationIdentifierLinkList(GenericIdentifierLinkList):
    parent = Relation


class RelationIdentifierLinkDetail(GenericIdentifierLinkDetail):
    parent = Relation


class RelationCitationListCreateView(BaseCitationListCreateView):
    entity = Relation


class RelationCitationDetailView(BaseCitationDetailView):
    entity = Relation


class RelationFieldCitationView(BaseFieldCitationView):
    entity = Relation


class RelationContactDetailFieldCitationView(GenericContactDetailFieldCitationView):
    parent = Relation


class RelationIdentifierCitationListView(GenericIdentifierCitationListView):
    parent = Relation


class RelationIdentifierCitationDetailView(GenericIdentifierCitationDetailView):
    parent = Relation


class RelationIdentifierFieldCitationView(GenericIdentifierFieldCitationView):
    parent = Relation
