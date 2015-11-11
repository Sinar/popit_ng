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


class PostList(APIView):

    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def get(self, request, language, format=None):

        posts = Post.objects.untranslated().all()
        serializer = PostSerializer(posts, many=True, language=language)
        return Response(serializer.data)

    def post(self, request, language, format=None):
        serializer = PostSerializer(data=request.data, language=language)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):

    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

    def get_object(self, pk):
        try:
            return Post.objects.untranslated().get(id=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, language, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post, language=language)
        return Response(serializer.data)

    def put(self, request, language, pk, format=None):
        post= self.get_object(pk)
        serializer = PostSerializer(post, data=request.data, partial=True, language=language)
        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, language, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostContactDetailDetail(GenericContactDetailDetail):
    parent = Post


class PostContactDetailList(GenericContactDetailList):
    parent = Post


class PostContactDetailLinkDetail(GenericContactDetailLinkDetail):
    parent = Post


class PostContactDetailLinkList(GenericContactDetailLinkList):
    parent = Post


# Because the specification uses other_label but It is easier to just use OtherName object Yes I am lazy
class PostOtherLabelsDetail(APIView):

    permission_classes = (
        IsAuthenticatedOrReadOnly,
    )

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
        return Response(serializer.data)

    def put(self, request, language, parent_pk, pk, format=None):
        other_labels = self.get_object(parent_pk, pk)
        serializer = OtherNameSerializer(other_labels, data=request.data, language=language)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, language, parent_pk, pk, format=None):
        other_labels = self.get_object(parent_pk, pk)
        other_labels.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostOtherLabelsList(APIView):

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
        serializer = OtherNameSerializer(other_labels, many=True, language=language)
        return Response(serializer.data)

    def post(self, request, language, parent_pk):
        post = Post.objects.untranslated().get(id=parent_pk)
        serializer = OtherNameSerializer(data=request.data, language=language)
        if serializer.is_valid():
            serializer.save(content_object=post)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostOtherLabelsLinkDetail(GenericOtherNameLinkDetail):
    parent = Post


class PostOtherLabelsLinkList(GenericOtherNameLinkList):
    parent = Post


class PostLinkDetail(GenericLinkDetail):
    parent = Post


class PostLinkList(GenericLinkList):
    parent = Post