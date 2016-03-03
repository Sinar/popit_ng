__author__ = 'sweemeng'
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from popit.models import Area
from django.db.models.signals import post_save
from django.db.models.signals import pre_delete
from popit.signals.handlers import *
from popit.models import *


class AreaAPITestCase(APITestCase):
    fixtures = [ "api_request_test_data.yaml" ]

    def setUp(self):
        post_save.disconnect(person_save_handler, Person)
        post_save.disconnect(organization_save_handler, Organization)
        post_save.disconnect(membership_save_handler, Membership)
        post_save.disconnect(post_save_handler, Post)
        post_save.disconnect(othername_save_handler, OtherName)
        post_save.disconnect(identifier_save_handler, Identifier)
        post_save.disconnect(contactdetail_save_handler, ContactDetail)
        post_save.disconnect(link_save_handler, Link)

    def tearDown(self):
        post_save.connect(person_save_handler, Person)
        post_save.connect(organization_save_handler, Organization)
        post_save.connect(membership_save_handler, Membership)
        post_save.connect(post_save_handler, Post)
        post_save.connect(othername_save_handler, OtherName)
        post_save.connect(identifier_save_handler, Identifier)
        post_save.connect(contactdetail_save_handler, ContactDetail)
        post_save.connect(link_save_handler, Link)

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


class AreaLinkAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]
    def setUp(self):
        post_save.disconnect(person_save_handler, Person)
        post_save.disconnect(organization_save_handler, Organization)
        post_save.disconnect(membership_save_handler, Membership)
        post_save.disconnect(post_save_handler, Post)
        post_save.disconnect(othername_save_handler, OtherName)
        post_save.disconnect(identifier_save_handler, Identifier)
        post_save.disconnect(contactdetail_save_handler, ContactDetail)
        post_save.disconnect(link_save_handler, Link)

    def tearDown(self):
        post_save.connect(person_save_handler, Person)
        post_save.connect(organization_save_handler, Organization)
        post_save.connect(membership_save_handler, Membership)
        post_save.connect(post_save_handler, Post)
        post_save.connect(othername_save_handler, OtherName)
        post_save.connect(identifier_save_handler, Identifier)
        post_save.connect(contactdetail_save_handler, ContactDetail)
        post_save.connect(link_save_handler, Link)

    def test_list_area_link(self):
        response = self.client.get("/en/areas/640c0f1d-2305-4d17-97fe-6aa59f079cc4/links/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_area_link_not_exist(self):
        response = self.client.get("/en/areas/640c0f1d-2305-4d17-97fe-6aa59f079cc4/links/not_exists/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_show_area_link(self):
        response = self.client.get("/en/areas/640c0f1d-2305-4d17-97fe-6aa59f079cc4/links/ed8a52d8-5503-45aa-a2ad-9931461172d2/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_area_link_unauthorized(self):
        data = {
            "url": "http://www.google.com",
            "note": "just a link"
        }
        response = self.client.post("/en/areas/640c0f1d-2305-4d17-97fe-6aa59f079cc4/links/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_area_link_authorized(self):
        data = {
            "url": "http://www.google.com",
            "note": "just a link"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/areas/640c0f1d-2305-4d17-97fe-6aa59f079cc4/links/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_area_link_not_exist_unauthorized(self):
        data = {
            "id": "ed8a52d8-5503-45aa-a2ad-9931461172d2",
            "note": "just a link"
        }
        response = self.client.put("/en/areas/640c0f1d-2305-4d17-97fe-6aa59f079cc4/links/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_area_link_not_exist_authorized(self):
        data = {
            "id": "ed8a52d8-5503-45aa-a2ad-9931461172d2",
            "note": "just a link"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/areas/640c0f1d-2305-4d17-97fe-6aa59f079cc4/links/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_area_link_unauthorized(self):
        data = {
            "id": "ed8a52d8-5503-45aa-a2ad-9931461172d2",
            "note": "just a link"
        }
        response = self.client.put(
            "/en/areas/640c0f1d-2305-4d17-97fe-6aa59f079cc4/links/ed8a52d8-5503-45aa-a2ad-9931461172d2/", data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_area_link_authorized(self):
        data = {
            "id": "ed8a52d8-5503-45aa-a2ad-9931461172d2",
            "note": "just a link"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/areas/640c0f1d-2305-4d17-97fe-6aa59f079cc4/links/ed8a52d8-5503-45aa-a2ad-9931461172d2/", data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_area_link_not_exist_unauthorized(self):
        response = self.client.delete("/en/areas/640c0f1d-2305-4d17-97fe-6aa59f079cc4/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_area_link_not_exist_authrozied(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/areas/640c0f1d-2305-4d17-97fe-6aa59f079cc4/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_area_link_unauthorized(self):
        response = self.client.delete("/en/areas/640c0f1d-2305-4d17-97fe-6aa59f079cc4/links/ed8a52d8-5503-45aa-a2ad-9931461172d2/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_area_link_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/areas/640c0f1d-2305-4d17-97fe-6aa59f079cc4/links/ed8a52d8-5503-45aa-a2ad-9931461172d2/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



