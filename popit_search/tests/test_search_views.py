from rest_framework.test import APITestCase
from rest_framework import status
from popit_search.utils.search import popit_indexer
from popit_search.utils.search import remove_popit_index


class SearchAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    def setUp(self):
        remove_popit_index()
        popit_indexer()

    def tearDown(self):
        remove_popit_index()
        popit_indexer()

    def test_person_search(self):
        params = {
            "q": "id:8497ba86-7485-42d2-9596-2ab14520f1f4"
        }
        response = self.client.get("/en/search/persons/", params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, [])

    def test_organization_search(self):
        params = {
            "q": "id:3d62d9ea-0600-4f29-8ce6-f7720fd49aa3"
        }
        response = self.client.get("/en/search/organizations/", params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, [])

    def test_membership_search(self):
        params = {
            "q": "id:b351cdc2-6961-4fc7-9d61-08fca66e1d44"
        }
        response = self.client.get("/en/search/memberships/", params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, [])

    def test_post_search(self):
        params = {
            "q": "id:c1f0f86b-a491-4986-b48d-861b58a3ef6e"
        }
        response = self.client.get("/en/search/posts/", params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data, [])

