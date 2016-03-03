from django.shortcuts import render
from rest_framework.views import APIView
from popit_search.utils.search import SerializerSearch
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ParseError
import logging
from popit.views.base import BasePopitView
from popit.models import Organization
from popit.models import Person
from popit.models import Post
from popit.models import Membership
from popit.serializers import OrganizationSerializer
from popit.serializers import PersonSerializer
from popit.serializers import PostSerializer
from popit.serializers import MembershipSerializer

ES_MODEL_MAP = {
    "organizations": Organization,
    "persons": Person,
    "posts": Post,
    "memberships": Membership,
}

ES_SERIALIZER_MAP = {
    "organizations": OrganizationSerializer,
    "persons": PersonSerializer,
    "posts": PostSerializer,
    "memberships": MembershipSerializer,
}

# Create your views here.
class GenericSearchView(BasePopitView):
    index = None

    def get(self, request, language, index_name, **kwargs):
        search = SerializerSearch(index_name)

        q = request.GET.get("q")
        logging.warn(q)
        if not q:
            raise ParseError("q parameter is required, data format can be found at https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html")

        instance = ES_MODEL_MAP.get(index_name)
        if not instance:
            raise EntityNotIndexedException("Entity not indexed or entity is not valid")

        result = search.search(query=q, language=language)

        output = []

        for item in result:
            try:
                entity = instance.objects.language(language).get(id=item["id"])
                serializer_class = ES_SERIALIZER_MAP[index_name]
                serializer = serializer_class(entity, language=language)
                output.append(serializer.data)
            except instance.DoesNotExist:
                continue

        page = self.paginator.paginate_queryset(output, request, view=self)
        return self.paginator.get_paginated_response(page)


class EntityNotIndexedException(Exception):
    pass