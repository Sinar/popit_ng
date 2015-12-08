from django.shortcuts import render
from rest_framework.views import APIView
from popit_search.utils.search import SerializerSearch
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
import logging
from popit.views.base import BasePopitView


# Create your views here.
class GenericSearchView(BasePopitView):
    index = None

    def get(self, request, language, index_name, **kwargs):
        search = SerializerSearch(index_name)

        q = request.GET.get("q")
        logging.warn(q)
        result = search.search(query=q, language=language)
        page = self.paginator.paginate_queryset(result, request, view=self)
        return self.paginator.get_paginated_response(page)
