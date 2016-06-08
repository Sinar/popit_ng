from popit_search.utils import search
from rest_framework.settings import api_settings


class PaginatedSearchUtil(object):
    def __init__(self, entity):
        self.page_size = api_settings.PAGE_SIZE
        self.search = search.SerializerSearch(entity)

    def views(self):
        pass