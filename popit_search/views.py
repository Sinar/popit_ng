from django.shortcuts import render
from rest_framework.views import APIView
from popit_search.utils.search import SerializerSearch
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ParseError
import logging
from popit.views.base import BasePopitView
from popit.models import Organization
from popit.models import Person
from popit.models import Post
from popit.models import Membership
from popit.models import Identifier
from popit.models import ContactDetail
from popit.models import OtherName
from popit.models import Link
from popit.serializers import OrganizationSerializer
from popit.serializers import PersonSerializer
from popit.serializers import PostSerializer
from popit.serializers import MembershipSerializer

ES_MODEL_MAP = {
    "organizations": Organization,
    "persons": Person,
    "posts": Post,
    "memberships": Membership,
    "identifiers": Identifier,
    "other_names": OtherName,
    "links": Link,
    "contact_details": ContactDetail,
    "parent": Organization,
    "other_labels": OtherName
}

ES_SERIALIZER_MAP = {
    "organizations": OrganizationSerializer,
    "persons": PersonSerializer,
    "posts": PostSerializer,
    "memberships": MembershipSerializer,
}


# TODO: We need to fix and deprecate this shit
class ResultFilters(object):
    def filter_result(self, result, index_name, language):
        entity = ES_MODEL_MAP.get(index_name)
        if not entity:
            raise EntityNotIndexedException("Entity not indexed or entity is not valid")
        output = []

        for item in result:

            instance = self.filter_instance(entity, item["id"], language)
            if instance:
                serializer_class = ES_SERIALIZER_MAP[index_name]
                serializer = serializer_class(instance, language=language)
                output.append(serializer.data)

        return output

    def filter_instance(self, entity, instance_id, language):
        try:
            instance = entity.objects.language(language).get(id=instance_id)
            return instance
        except entity.DoesNotExist:
            return None

    def filter_nested(self, item, language):
        for key in item:
            if key in ES_MODEL_MAP:
                if type(item[key]) is list:
                    temp = []
                    for entry in item[key]:
                        entity = ES_MODEL_MAP[key]
                        instance = self.filter_instance(entity, entry["id"], language)
                        if instance:
                            temp.append(entry)
                    item[key] = temp
                elif type(item[key]) is dict:
                    entity = ES_MODEL_MAP[key]
                    instance = self.filter_instance(entity, item[key]["id"], language)
                    if not instance:
                        item[key] = {}
        return item

    # This is used on cleaned data
    def drop_result(self, entry, query):
        keys, value = self.parse_query(query)
        check = entry
        for key in keys:

            if issubclass(type(check), list):
                matched = False
                for item in check:
                    if value.lower() in item[key].lower():
                        matched = True
                if not matched:
                    return True
                else:
                    return False

            elif issubclass(type(check), dict):
                # we are not sure if the next item is a list or not. Should not because I limit the depth
                check = entry[key]

        # Because last key in the dict. Loop will end, so check for value
        if value.lower() not in check:
            return True
        return False

    def parse_query(self, query):

        q = query.split(":")
        if len(q) > 1:

            key, value = q
            keys = key.split(".")
            return keys, value
        else:
            return [], q[0]


# Create your views here.
class GenericSearchView(BasePopitView, ResultFilters):
    index = None

    def get(self, request, language, index_name, **kwargs):
        search = SerializerSearch(index_name)

        q = request.GET.get("q")
        logging.warn(q)
        if not q:
            raise ParseError("q parameter is required, data format can be found at https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html")

        result = search.paginated_search(q, request, language)
        return result


class GenericRawSearchView(BasePopitView):
    index = None

    def get(self, request, **kwargs):
        search = SerializerSearch(None)
        q = request.GET.get("q")
        if not q:
            raise ParseError(
                "q parameter is required, data format can be found at https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html")
        result = search.raw_query(q)
        return Response(result)

    def post(self, request, **kwargs):
        data = request.data
        search = SerializerSearch(None)
        result = search.raw_query(query_body=data)
        return Response(result)


class AdvanceSearchView(APIView):
    permission_classes = (
        AllowAny,
    )

    def get(self, request, entity, **kwargs):
        search = SerializerSearch(None)
        q = request.query_params.get("q")
        size = request.query_params.get("size", "10")
        from_ = request.query_params.get("from", "0")
        if not q:
            raise ParseError(
                "q parameter is required, data format can be found at https://www.elastic.co/guide/en/elasticsearch/reference/current/search-search.html")
        result = search.raw_query(query=q, entity=entity, size=int(size), from_=int(from_))
        return Response(result)

    def post(self, request, entity, **kwargs):
        data = request.data
        
        size = request.query_params.get("size", "10")
        from_ = request.query_params.get("from", "0")
        search = SerializerSearch(None)
        result = search.raw_query(query_body=data, entity=entity, size=int(size), from_=int(from_))
        return Response(result)


class EntityNotIndexedException(Exception):
    pass


class OperationNotSupportedException(Exception):
    pass