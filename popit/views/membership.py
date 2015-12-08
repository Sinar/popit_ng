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


class MembershipList(BasePopitListCreateView):
    serializer = MembershipSerializer
    entity = Membership


class MembershipDetail(BasePopitDetailUpdateView):

    serializer = MembershipSerializer
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