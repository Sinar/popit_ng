from rest_framework.test import APITestCase
from rest_framework import status
from popit.models import ContactDetail
from popit.models import Link
from rest_framework.authtoken.models import Token


class MembershipContactDetailAPI(APITestCase):
    fixtures = [ "api_request_test_data.yaml" ]

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