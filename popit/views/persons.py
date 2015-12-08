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
