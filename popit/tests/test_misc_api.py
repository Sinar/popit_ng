__author__ = 'sweemeng'
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from popit.models import Area


class AreaAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    def test_view_area_list(self):
        response = self.client.get("/en/areas/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_area_detail(self):
        response = self.client.get("/en/areas/640c0f1d-2305-4d17-97fe-6aa59f079cc4/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_area_detail_not_exist(self):
        response = self.client.get("/en/areas/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_area_unauthorized(self):
        data = {
           "name": "timbuktu"
        }
        response = self.client.post("/en/areas/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_area_authorized(self):
        data = {
           "name": "timbuktu"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/areas/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_area_not_exist_unauthorized(self):
        data = {
           "classification": "city"
        }
        response = self.client.put("/en/areas/not_exists/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_area_not_exist_authorized(self):
        data = {
           "classification": "city"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/areas/not_exists/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_area_unauthorized(self):
        data = {
           "classification": "city"
        }
        response = self.client.put("/en/areas/640c0f1d-2305-4d17-97fe-6aa59f079cc4/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_area_authorized(self):
        data = {
           "classification": "city"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/areas/640c0f1d-2305-4d17-97fe-6aa59f079cc4/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_area_not_exist_unauthorized(self):
        response = self.client.delete("/en/areas/not_exists/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_area_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/areas/not_exists/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_area_unauthorized(self):
        response = self.client.delete("/en/areas/640c0f1d-2305-4d17-97fe-6aa59f079cc4/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_area_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/areas/640c0f1d-2305-4d17-97fe-6aa59f079cc4/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)





