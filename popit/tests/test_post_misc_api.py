__author__ = 'sweemeng'
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from popit.signals.handlers import *
from popit.models import *


class PostOtherLabelsAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    def setUp(self):
        post_save.disconnect(person_save_handler, Person)
        pre_delete.disconnect(person_delete_handler, Person)
        post_save.disconnect(organization_save_handler, Organization)
        pre_delete.disconnect(organization_delete_handler, Organization)
        post_save.disconnect(membership_save_handler, Membership)
        pre_delete.disconnect(membership_delete_handler, Membership)
        post_save.disconnect(post_save_handler, Post)
        pre_delete.disconnect(post_delete_handler, Post)

    def tearDown(self):
        post_save.connect(person_save_handler, Person)
        pre_delete.connect(person_delete_handler, Person)
        post_save.connect(organization_save_handler, Organization)
        pre_delete.connect(organization_delete_handler, Organization)
        post_save.connect(membership_save_handler, Membership)
        pre_delete.connect(membership_delete_handler, Membership)
        post_save.connect(post_save_handler, Post)
        pre_delete.connect(post_delete_handler, Post)

    def test_list_post_otherlabels_api(self):
        response = self.client.get("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_post_ther_labels_api_not_exist_unauthorized(self):
        response = self.client.get("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/not_exists/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_show_post_other_labels_api_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/not_exists/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_show_other_labels_api_exist_unauthorized(self):

        response = self.client.get("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/aee39ddd-6785-4a36-9781-8e745c6359b7/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_other_labels_api_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.get("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/aee39ddd-6785-4a36-9781-8e745c6359b7/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_other_labels_api_unauthroized(self):
        data = {
            "name": "sampan party"
        }
        response = self.client.post("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_other_labels_api_authroized(self):
        data = {
            "name": "sampan party"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_post_other_labels_api_exist_unauthorized(self):
        data = {
            "name": "Bilge Rat"
        }
        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/aee39ddd-6785-4a36-9781-8e745c6359b7/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_other_labels_api_not_exist_unauthorized(self):
        data = {
            "name": "Bilge Rat"
        }
        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_other_labels_api_exist_authorized(self):
        data = {
            "name": "Bilge Rat"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/aee39ddd-6785-4a36-9781-8e745c6359b7/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post_other_labels_api_not_exist_authorized(self):
        data = {
            "name": "Bilge Rat"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_post_other_labels_api_not_exist_unauthorized(self):
        response = self.client.delete("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_other_labels_api_exist_unauthorized(self):
        response = self.client.delete("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/aee39ddd-6785-4a36-9781-8e745c6359b7/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_other_labels_api_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_post_other_labels_api_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/aee39ddd-6785-4a36-9781-8e745c6359b7/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PostContactDetailsAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    def setUp(self):
        post_save.disconnect(person_save_handler, Person)
        pre_delete.disconnect(person_delete_handler, Person)
        post_save.disconnect(organization_save_handler, Organization)
        pre_delete.disconnect(organization_delete_handler, Organization)
        post_save.disconnect(membership_save_handler, Membership)
        pre_delete.disconnect(membership_delete_handler, Membership)
        post_save.disconnect(post_save_handler, Post)
        pre_delete.disconnect(post_delete_handler, Post)

    def tearDown(self):
        post_save.connect(person_save_handler, Person)
        pre_delete.connect(person_delete_handler, Person)
        post_save.connect(organization_save_handler, Organization)
        pre_delete.connect(organization_delete_handler, Organization)
        post_save.connect(membership_save_handler, Membership)
        pre_delete.connect(membership_delete_handler, Membership)
        post_save.connect(post_save_handler, Post)
        pre_delete.connect(post_delete_handler, Post)

    def test_list_post_contact_detaills(self):
        response = self.client.get("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_post_contact_details_exist(self):
        response = self.client.get("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/7f3f67c4-6afd-4de9-880e-943560cf56c0/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_post_contact_details_not_exist(self):
        response = self.client.get("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_post_contact_detail_unauthorized(self):
        data = {
            "type": "sms",
            "value": "231313123131",
        }

        response = self.client.post("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_contact_detail_authorized(self):
        data = {
            "type": "sms",
            "value": "231313123131",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_post_contact_detail_not_exist_unauthorized(self):
        data = {
            "id": "7f3f67c4-6afd-4de9-880e-943560cf56c0",
            "type": "phone"
        }
        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_contact_detail_not_exist_authorized(self):
        data = {
            "id": "7f3f67c4-6afd-4de9-880e-943560cf56c0",
            "type": "phone"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_post_contact_detail_exist_unauthorized(self):
        data = {
            "id": "7f3f67c4-6afd-4de9-880e-943560cf56c0",
            "type": "phone"
        }
        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/7f3f67c4-6afd-4de9-880e-943560cf56c0/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_contact_detail_exist_authorized(self):
        data = {
            "id": "7f3f67c4-6afd-4de9-880e-943560cf56c0",
            "type": "phone"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/7f3f67c4-6afd-4de9-880e-943560cf56c0/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post_contact_detail_not_exist_unauthorized(self):
        response = self.client.delete("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/not_exist/")
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_contact_detail_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/not_exist/")
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)

    def test_delete_post_contact_detail_exist_unauthorized(self):
        response = self.client.delete("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/7f3f67c4-6afd-4de9-880e-943560cf56c0/")
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_contact_detail_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/7f3f67c4-6afd-4de9-880e-943560cf56c0/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PostListAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    def setUp(self):
        post_save.disconnect(person_save_handler, Person)
        pre_delete.disconnect(person_delete_handler, Person)
        post_save.disconnect(organization_save_handler, Organization)
        pre_delete.disconnect(organization_delete_handler, Organization)
        post_save.disconnect(membership_save_handler, Membership)
        pre_delete.disconnect(membership_delete_handler, Membership)
        post_save.disconnect(post_save_handler, Post)
        pre_delete.disconnect(post_delete_handler, Post)

    def tearDown(self):
        post_save.connect(person_save_handler, Person)
        pre_delete.connect(person_delete_handler, Person)
        post_save.connect(organization_save_handler, Organization)
        pre_delete.connect(organization_delete_handler, Organization)
        post_save.connect(membership_save_handler, Membership)
        pre_delete.connect(membership_delete_handler, Membership)
        post_save.connect(post_save_handler, Post)
        pre_delete.connect(post_delete_handler, Post)

    def test_list_post_link(self):
        response = self.client.get("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/links/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_post_links_not_exist(self):
        response = self.client.get("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_show_post_links_exist(self):
        response = self.client.get("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/links/ce15a9ee-6742-4467-bbfb-c86459ee685b/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_links_unauthorized(self):
        data = {
            "url": "http://www.yahoo.com"
        }

        response = self.client.post("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/links/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_links_authorized(self):
        data = {
            "url": "http://www.yahoo.com"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/links/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_post_links_exist_unauthorized(self):
        data = {
            "note": "just a link"
        }
        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/links/ce15a9ee-6742-4467-bbfb-c86459ee685b/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_links_not_exist_unauthorized(self):
        data = {
            "note": "just a link"
        }
        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/links/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_links_exist_authorized(self):
        data = {
            "note": "just a link"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/links/ce15a9ee-6742-4467-bbfb-c86459ee685b/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post_links_not_exist_authorized(self):
        data = {
        "note": "just a link"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/links/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_post_links_not_exist_unauthorized(self):
        response = self.client.delete("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_links_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_post_links_exist_unauthorized(self):
        response = self.client.delete("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/links/ce15a9ee-6742-4467-bbfb-c86459ee685b/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_poost_links_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/links/ce15a9ee-6742-4467-bbfb-c86459ee685b/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)