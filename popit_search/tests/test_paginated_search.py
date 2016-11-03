from mock import patch
from django.test import TestCase
from django.test import override_settings
from django.test.client import RequestFactory
from popit_search.utils import search
from popit.models import Person
from popit.serializers import PersonSerializer


class PaginatedSearch(TestCase):
    def setUp(self):

        self.factory = RequestFactory()

    @patch("elasticsearch.Elasticsearch")
    def test_page_size(self, mock_es):
        instance = mock_es.return_value
        s = search.SerializerSearch("persons")
        # We are on default page size of 10
        # If we have 20 item, then we have 2 page
        page = s.get_page(20)
        self.assertEqual(page, 2)

    @patch("elasticsearch.Elasticsearch")
    def test_get_page_start(self, mock_es):
        instance = mock_es.return_value
        s = search.SerializerSearch("persons")

        current_page = 2
        start = s.get_start(current_page - 1)
        self.assertEqual(start, 10)

    @patch("elasticsearch.Elasticsearch")
    def test_has_more(self, mock_es):
        instance = mock_es.return_value
        s = search.SerializerSearch("persons")

        s.result_count = 100
        has_more = s.has_more(10)
        self.assertFalse(has_more)

    @patch("elasticsearch.Elasticsearch")
    def test_next_page(self, mock_es):
        instance = mock_es.return_value
        s = search.SerializerSearch("persons")
        current_page = 2
        s.result_count = 100
        next_page = s.get_next_page(current_page)

        self.assertEqual(next_page, 3)

    @patch("elasticsearch.Elasticsearch")
    def test_next_page_none(self, mock_es):
        instance = mock_es.return_value
        s = search.SerializerSearch("persons")
        current_page = 2
        s.result_count = 10
        next_page = s.get_next_page(current_page)

        self.assertEqual(next_page, None)

    @patch("elasticsearch.Elasticsearch")
    def test_prev_page(self, mock_es):
        instance = mock_es.return_value
        s = search.SerializerSearch("persons")
        current_page = 2
        prev_page = s.get_prev_page(current_page)

        self.assertEqual(prev_page, 1)

    @patch("elasticsearch.Elasticsearch")
    def test_prev_page_none(self, mock_es):
        instance = mock_es.return_value
        s = search.SerializerSearch("persons")
        current_page = 1
        prev_page = s.get_prev_page(current_page)

        self.assertEqual(prev_page, None)

    @patch("elasticsearch.Elasticsearch")
    def test_get_links(self, mock_es):
        instance = mock_es.return_value
        request = self.factory.get("/en/search/persons/?q=id:121213&page=1")
        s = search.SerializerSearch("persons")
        url = s.get_links(request, 5)
        self.assertEqual("http://testserver/en/search/persons/?q=id%3A121213&page=5", url)

    @patch("elasticsearch.Elasticsearch")
    def test_get_links_i18f(self, mock_es):
        instance = mock_es.return_value
        request = self.factory.get("/en/search/persons/?q=name:%E1%80%A1%E1%80%B1%E1%80%AC%E1%80%84%E1%80%BA*")
        s = search.SerializerSearch("persons")
        url = s.get_links(request, 5)
        self.assertEqual("http://testserver/en/search/persons/?q=name%3A%E1%80%A1%E1%80%B1%E1%80%AC%E1%80%84%E1%80%BA%2A&page=5", url)

