from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from popit.signals.handlers import *
from popit.models import *


class MembershipAPITestCasse(APITestCase):
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

    def test_list_membership(self):
        response = self.client.get("/en/memberships/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_membership_detail(self):
        response = self.client.get("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_membership_detail_not_exist(self):
        response = self.client.get("/en/memberships/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_membership_unauthorized(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec"
        }
        response = self.client.post("/en/memberships/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_membership_authorized(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/memberships/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_membership_without_post_organization_unauthorized(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
        }

        response = self.client.post("/en/memberships/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_membership_without_post_organization_authorized(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/memberships/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_membership_with_post_unauthorized(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "post_id": "c1f0f86b-a491-4986-b48d-861b58a3ef6e"
        }

        response = self.client.post("/en/memberships/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_membership_with_post_authorized(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "post_id": "c1f0f86b-a491-4986-b48d-861b58a3ef6e"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/memberships/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_membership_with_organization_unauthorized(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec"
        }
        response = self.client.post("/en/memberships/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_membership_with_organization_authorized(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/memberships/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_membership_conflict_organization_post_organization_unauthorized(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec",
            "post_id": "c1f0f86b-a491-4986-b48d-861b58a3ef6e"
        }
        response = self.client.post("/en/memberships/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_membership_conflict_organization_post_organization_authorized(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec",
            "post_id": "c1f0f86b-a491-4986-b48d-861b58a3ef6e"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/memberships/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_membership_unauthorized(self):
        data = {
            "label": "sweemeng land lubber"
        }

        response = self.client.put("/en/memberships/0a44195b-c3c9-4040-8dbf-be1aa250b700/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_membership_not_exist_unauthorized(self):
        data = {
            "label": "sweemeng land lubber"
        }

        response = self.client.put("/en/memberships/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_membership_authorized(self):
        data = {
            "label": "sweemeng land lubber"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/memberships/0a44195b-c3c9-4040-8dbf-be1aa250b700/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_membership_not_exist_authorized(self):
        data = {
            "label": "sweemeng land lubber"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/memberships/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_membership_conlict_post_organization_unauthorized(self):
        data = {
            "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec"
        }
        response = self.client.put("/en/memberships/0a44195b-c3c9-4040-8dbf-be1aa250b700/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_membership_conlict_post_organization_authorized(self):
        data = {
            "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/memberships/0a44195b-c3c9-4040-8dbf-be1aa250b700/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_membership_conflict_organization_post_unauthorized(self):
        data = {
            "post_id":"3eb967bb-23e3-41b6-8cba-54aadac8d918"
        }
        response = self.client.put("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_membership_conflict_organization_post_authorized(self):
        data = {
            "post_id":"3eb967bb-23e3-41b6-8cba-54aadac8d918"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_membership_contact_unauthorized(self):
        data = {
            "contact_details": [
                {
                    "type": "phone",
                    "value": "755-2525",
                    "label": "captain's phone"
                }
            ]
        }
        response = self.client.put("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_membership_contact_authorized(self):

        data = {
            "contact_details": [
                {
                    "type": "phone",
                    "value": "755-2525",
                    "label": "captain's phone"
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_membership_contact_unauthorized(self):
        data = {
            "contact_details": [
                {
                    "id": "78a35135-52e3-4af9-8c32-ea3f557354fd",
                    "label": "captain's email"
                }
            ]
        }
        response = self.client.put("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_membership_contact_authorized(self):
        data = {
            "contact_details": [
                {
                    "id": "78a35135-52e3-4af9-8c32-ea3f557354fd",
                    "label": "captain's email"
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_membership_link_unauthorized(self):
        data = {
            "links": [
                {
                    "url": "http://thecaptain.tumblr.com",
                    "label": "Captain's Tumblr"
                }
            ]
        }

        response = self.client.put("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_membership_link_authorized(self):
        data = {
            "links": [
                {
                    "url": "http://thecaptain.tumblr.com",
                    "label": "Captain's Tumblr"
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_membership_link_unauthorized(self):
        data = {
            "links": [
                {
                    "id": "239edef4-af68-4ffb-adce-96d17cbea79d",
                    "label": "Captain's page"
                }
            ]
        }
        response = self.client.put("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_membership_link_authorized(self):
        data = {
            "links": [
                {
                    "id": "239edef4-af68-4ffb-adce-96d17cbea79d",
                    "label": "Captain's page"
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_membership_unauthorized(self):
        response = self.client.delete("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_membership_not_exist_unauthorized(self):
        response = self.client.delete("/en/memberships/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_membership_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_membership_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/memberships/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fetch_membership_translated_nested(self):
        response = self.client.get("/ms/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/")
        results = response.data["result"]

        self.assertEqual(results["organization"]["name"], "Parti Lanun KL")
        self.assertEqual(results["organization"]["language_code"], "ms")

    def test_fetch_membership_translated(self):
        response = self.client.get("/ms/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/")
        results = response.data["result"]
        self.assertEqual(results["label"], "Kapten Jolly Roger")
        self.assertEqual(results["language_code"], "ms")

    def test_create_membership_invalid_date(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec",
            "start_date": "invalid date",
            "end_date": "invalid date"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/memberships/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_membership_valid_date(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec",
            "start_date": "2010-01-01",
            "end_date": "2015-01-01"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/memberships/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)