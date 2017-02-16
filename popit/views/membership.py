from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import Http404
from popit.models import Membership
from popit.views.misc import GenericContactDetailDetail
from popit.views.misc import GenericContactDetailList
from popit.views.misc import GenericContactDetailLinkDetail
from popit.views.misc import GenericContactDetailLinkList
from popit.views.misc import GenericLinkDetail
from popit.views.misc import GenericLinkList
from popit.serializers import MembershipSerializer
from popit.views.base import BasePopitDetailUpdateView
from popit.views.base import BasePopitListCreateView
from popit.views.citation import BaseCitationDetailView
from popit.views.citation import BaseCitationListCreateView
from popit.views.citation import GenericContactDetailCitationDetailView
from popit.views.citation import GenericContactDetailCitationListView
from popit.views.citation import BaseFieldCitationView
from popit.views.citation import GenericContactDetailFieldCitationView
from popit.serializers.minimized import MinMembershipSerializer


class MembershipList(BasePopitListCreateView):
    serializer = MembershipSerializer
    mini_serializer = MinMembershipSerializer
    entity = Membership


class MembershipDetail(BasePopitDetailUpdateView):

    serializer = MembershipSerializer
    mini_serializer = MinMembershipSerializer
    entity = Membership


class MembershipContactDetailDetail(GenericContactDetailDetail):
    parent = Membership


class MembershipContactDetailList(GenericContactDetailList):
    parent = Membership


class MembershipContactDetailLinkDetail(GenericContactDetailLinkDetail):
    parent = Membership


class MembershipContactDetailLinkList(GenericContactDetailLinkList):
    parent = Membership


class MembershipLinkDetail(GenericLinkDetail):
    parent = Membership


class MembershipLinkList(GenericLinkList):
    parent = Membership


class MembershipCitationListCreateView(BaseCitationListCreateView):
    entity = Membership


class MembershipCitationDetailView(BaseCitationDetailView):
    entity = Membership


class MembershipContactDetailCitationListView(GenericContactDetailCitationListView):
    parent = Membership


class MembershipContactDetailCitationDetailView(GenericContactDetailCitationDetailView):
    parent = Membership


class MembershipFieldCitationView(BaseFieldCitationView):
    entity = Membership


class MembershipContactDetailFieldCitationView(GenericContactDetailFieldCitationView):
    parent = Membership
