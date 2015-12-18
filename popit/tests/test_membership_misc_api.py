from rest_framework.test import APITestCase
from rest_framework import status
from popit.models import ContactDetail
from popit.models import Link
from rest_framework.authtoken.models import Token
from popit.signals.handlers import *
from popit.models import *


class MembershipContactDetailAPI(APITestCase):
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

    def test_list_membership_contact_details_misc_api(self):
        response = self.client.get("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_membership_contact_details_details_misc_api(self):
        response = self.client.get("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/78a35135-52e3-4af9-8c32-ea3f557354fd/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_membership_contact_details_details_not_exist_misc_api(self):
        response = self.client.get("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_membership_contact_details_misc_api_unauthorized(self):
        data = {
            "type": "phone",
            "value": "755-2525",
            "label": "captain's phone"
        }
        response = self.client.post("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/",data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_membership_contact_details_misc_api_authorized(self):
        data = {
            "type": "phone",
            "value": "755-2525",
            "label": "captain's phone"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/",data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_membership_contact_detail_not_exist_unauthorized(self):
        data = {
            "label": "captain's email"
        }
        response = self.client.put("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/not_exist/",data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_membership_contact_detail_not_exist_authorized(self):
        data = {
            "label": "captain's email"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/not_exist/",data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_membership_contact_detail_exist_unauthorized(self):
        data = {
            "label": "captain's email"
        }
        response = self.client.put("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/78a35135-52e3-4af9-8c32-ea3f557354fd/",data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_membership_contact_detail_exist_authorized(self):
        data = {
            "label": "captain's email"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/78a35135-52e3-4af9-8c32-ea3f557354fd/",data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_membership_contact_detail_not_exist_unauthorized(self):
        response = self.client.delete("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_membership_contact_detail_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_membership_contact_detail_exist_unauthorized(self):
        response = self.client.delete("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/78a35135-52e3-4af9-8c32-ea3f557354fd/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_membership_contact_detail_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/78a35135-52e3-4af9-8c32-ea3f557354fd/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_create_membership_detail_invalid_date(self):
        data = {
            "type": "phone",
            "value": "755-2525",
            "label": "captain's phone",
            "valid_from": "invalid date",
            "valid_to": "invalid date",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/",data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_membership_detail_valid_date(self):
        data = {
            "type": "phone",
            "value": "755-2525",
            "label": "captain's phone",
            "valid_from": "2010-01-01",
            "valid_to": "2015-01-01",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/",data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class MembershipLinkAPITestCase(APITestCase):

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

    def test_list_membership_link_api(self):
        response = self.client.get("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/links/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_membership_link_detail_api(self):
        response = self.client.get("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/links/239edef4-af68-4ffb-adce-96d17cbea79d/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_membership_link_detail_api_not_exist(self):
        response = self.client.get("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_membership_link_api_unauthorized(self):
        data = {
            "url": "http://thecaptain.tumblr.com",
            "label": "Captain's Tumblr"
        }
        response = self.client.post("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/links/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_membership_link_api_authorized(self):
        data = {
            "url": "http://thecaptain.tumblr.com",
            "label": "Captain's Tumblr"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/links/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_membership_link_api_not_exist_unauthorized(self):
        data = {
            "id": "239edef4-af68-4ffb-adce-96d17cbea79d",
            "label": "Captain's page"
        }
        response = self.client.put("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/links/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_membership_link_api_not_exist_authorized(self):
        data = {
            "id": "239edef4-af68-4ffb-adce-96d17cbea79d",
            "label": "Captain's page"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/links/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_membership_link_api_exist_unauthorized(self):
        data = {
            "id": "239edef4-af68-4ffb-adce-96d17cbea79d",
            "label": "Captain's page"
        }
        response = self.client.put("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/links/239edef4-af68-4ffb-adce-96d17cbea79d/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_membership_link_api_exist_authorized(self):
        data = {
            "id": "239edef4-af68-4ffb-adce-96d17cbea79d",
            "label": "Captain's page"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/links/239edef4-af68-4ffb-adce-96d17cbea79d/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_membership_link_api_not_exist_unauthorized(self):
        response = self.client.delete("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_membership_link_api_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_membership_link_api_exist_unauthorized(self):
        response = self.client.delete("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/links/239edef4-af68-4ffb-adce-96d17cbea79d/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_membership_link_api_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/links/239edef4-af68-4ffb-adce-96d17cbea79d/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)