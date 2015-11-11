__author__ = 'sweemeng'
from rest_framework.test import APITestCase
from rest_framework import status


class PostOtherLabelsAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    def test_list_post_otherlabels_api(self):
        response = self.client.get("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
