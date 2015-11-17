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


class MembershipList(APIView):

    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def get(self, request, language, format=True):
        memberships = Membership.objects.untranslated().all()
        serializer = MembershipSerializer(memberships, many=True, language=language)

        return Response(serializer.data)

    def post(self, request, language, format=True):
        serializer = MembershipSerializer(data=request.data, language=language)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MembershipDetail(APIView):

    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def get_object(self, pk):
        try:
            return Membership.objects.untranslated().get(id=pk)
        except Membership.DoesNotExist:
            raise Http404

    def get(self, request, language, pk, format=True):
        membership = self.get_object(pk)
        serializer = MembershipSerializer(membership, language=language)
        return Response(serializer.data)

    def put(self, request, language, pk, format=True):
        membership = self.get_object(pk)
        serializer = MembershipSerializer(membership, data=request.data, partial=True, language=language)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, language, pk, format=True):
        membership = self.get_object(pk)
        membership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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