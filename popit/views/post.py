__author__ = 'sweemeng'
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.http import Http404
from popit.models import Post
from popit.models import OtherName
from popit.serializers import PostSerializer
from popit.serializers import OtherNameSerializer
from popit.views.misc import GenericContactDetailDetail
from popit.views.misc import GenericContactDetailLinkDetail
from popit.views.misc import GenericContactDetailLinkList
from popit.views.misc import GenericContactDetailList
from popit.views.misc import GenericOtherNameDetail
from popit.views.misc import GenericOtherNameLinkDetail
from popit.views.misc import GenericOtherNameLinkList
from popit.views.misc import GenericOtherNameList
from popit.views.misc import GenericLinkDetail
from popit.views.misc import GenericLinkList
from popit.views.base import BasePopitDetailUpdateView
from popit.views.base import BasePopitListCreateView
from popit.views.base import BasePopitView
from popit.views.citation import BaseCitationDetailView
from popit.views.citation import BaseCitationListCreateView
from popit.views.citation import GenericContactDetailCitationListView
from popit.views.citation import GenericContactDetailCitationDetailView
from popit.views.citation import BaseSubItemCitationListView
from popit.views.citation import BaseSubItemCitationDetailView
from popit.views.citation import BaseFieldCitationView
from popit.views.citation import GenericContactDetailFieldCitationView
from popit.views.citation import BaseSubItemFieldCitationView


class PostList(BasePopitListCreateView):

    entity = Post
    serializer = PostSerializer


class PostDetail(BasePopitDetailUpdateView):

    entity = Post
    serializer = PostSerializer


class PostContactDetailDetail(GenericContactDetailDetail):
    parent = Post


class PostContactDetailList(GenericContactDetailList):
    parent = Post


class PostContactDetailLinkDetail(GenericContactDetailLinkDetail):
    parent = Post


class PostContactDetailLinkList(GenericContactDetailLinkList):
    parent = Post


# Because the specification uses other_label but It is easier to just use OtherName object Yes I am lazy
class PostOtherLabelsDetail(BasePopitView):

    def get_object(self, parent_pk, pk):
        try:
            post = Post.objects.untranslated().get(id=parent_pk)
        except Post.DoesNotExist:
            raise Http404

        try:
            return post.other_labels.untranslated().get(id=pk)
        except OtherName.DoesNotExist:
            raise Http404

    def get(self, request, language, parent_pk, pk, format=None):
        other_labels = self.get_object(parent_pk, pk)
        serializer = OtherNameSerializer(other_labels, language=language)
        data = { "results": serializer.data }
        return Response(data)

    def put(self, request, language, parent_pk, pk, format=None):
        other_labels = self.get_object(parent_pk, pk)
        serializer = OtherNameSerializer(other_labels, data=request.data, language=language)
        if serializer.is_valid():
            serializer.save()
            data = { "results": serializer.data }
            return Response(data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, language, parent_pk, pk, format=None):
        other_labels = self.get_object(parent_pk, pk)
        other_labels.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostOtherLabelsList(BasePopitView):

    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def get_query(self, parent_pk):
        try:
            post = Post.objects.untranslated().get(id=parent_pk)
        except Post.DoesNotExist:
            raise Http404

        return post.other_labels.untranslated().all()

    def get(self, request, language, parent_pk):
        other_labels = self.get_query(parent_pk)
        page = self.paginator.paginate_queryset(other_labels, request, view=self)

        serializer = OtherNameSerializer(page, many=True, language=language)
        return self.paginator.get_paginated_response(serializer.data)

    def post(self, request, language, parent_pk):
        post = Post.objects.untranslated().get(id=parent_pk)
        serializer = OtherNameSerializer(data=request.data, language=language)
        if serializer.is_valid():
            serializer.save(content_object=post)
            data = { "results": serializer.data }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostOtherLabelsLinkDetail(GenericOtherNameLinkDetail):
    parent = Post


class PostOtherLabelsLinkList(GenericOtherNameLinkList):
    parent = Post


class PostLinkDetail(GenericLinkDetail):
    parent = Post


class PostLinkList(GenericLinkList):
    parent = Post


class PostCitationListCreateView(BaseCitationListCreateView):
    entity = Post


class PostCitationDetailView(BaseCitationDetailView):
    entity = Post


class PostContactDetailCitationListView(GenericContactDetailCitationListView):
    parent = Post


class PostContactDetailCitationDetailView(GenericContactDetailCitationDetailView):
    parent = Post


class PostOtherLabelsCitationListView(BaseSubItemCitationListView):
    parent = Post
    entity = OtherName

    def get_child(self, parent, child_pk, language):
        try:
            child = self.parent.other_labels.language(language).get(id=child_pk)
            return child
        except self.entity.DoesNotExist:
            raise Http404


class PostOtherLabelsCitationDetailView(BaseSubItemCitationDetailView):
    parent = Post
    entity = OtherName

    def get_child(self, parent, child_pk, language):
        try:
            child = self.parent.other_labels.language(language).get(id=child_pk)
            return child
        except self.entity.DoesNotExist:
            raise Http404


class PostFieldCitationView(BaseFieldCitationView):
    entity = Post


class PostContactDetailFieldCitationView(GenericContactDetailFieldCitationView):
    entity = Post


class PostOtherLabelFieldCitationView(BaseSubItemFieldCitationView):
    parent = Post
    entity = OtherName

    def get_child(self, parent, child_pk, language):
        try:
            child = self.parent.other_labels.language(language).get(id=child_pk)
            return child
        except self.entity.DoesNotExist:
            raise Http404
