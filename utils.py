from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class PopitPaginator(PageNumberPagination):
    page_number = 1

    def paginate_queryset(self, queryset, request, view=None):
        self.page_number = request.query_params.get(self.page_query_param, 1)
        result = super(PopitPaginator, self).paginate_queryset(queryset, request, view)
        return result

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('page', int(self.page_number)),
            ('total', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('per_page', self.page_size)
        ]))
