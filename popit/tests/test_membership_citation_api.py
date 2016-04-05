from rest_framework.test import APITestCase
from popit.signals.handlers import *
from popit.models import *
from rest_framework import status


class MembershipCitationAPITestCase(APITestCase):

    fixtures = ["api_request_test_data.yaml"]

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

    def test_fetch_membership_field_citation(self):
        response = self.client.get(
            "/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/citations/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_membership_citation_list(self):
        response = self.client.get(
            "/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/citations/label"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_membership_citation_detail(self):
        response = self.client.get(
            "/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/citations/label/b64a342357974502a26cc40d4cc85a78"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_membership_citation_unauthorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }
        response = self.client.post(
            "/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/citations/label",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_membership_citation_authorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            "/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/citations/label",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_membership_citation_unauthorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }

        response = self.client.put(
            "/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/citations/label/b64a342357974502a26cc40d4cc85a78",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_membership_citation_authorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/citations/label/b64a342357974502a26cc40d4cc85a78",
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_membership_citation_unauthorized(self):
        response = self.client.delete("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/citations/label/b64a342357974502a26cc40d4cc85a78")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_membership_citation_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/citations/label/b64a342357974502a26cc40d4cc85a78")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class MembershipContactDetailCitationAPITestCase(APITestCase):
    fixtures = ["api_request_test_data.yaml"]

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

    def test_fetch_membership_contactdetails_field_citations(self):
        response = self.client.get(
            "/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/78a35135-52e3-4af9-8c32-ea3f557354fd/citations/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_membership_contactdetails_citations_list(self):
        response = self.client.get(
            "/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/78a35135-52e3-4af9-8c32-ea3f557354fd/citations/label/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_membership_contactdetail_citation_detail(self):
        response = self.client.get(
            "/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/78a35135-52e3-4af9-8c32-ea3f557354fd/citations/label/09681352a2df465abe59d241b8693f07"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_membership_contactdetail_citation_detail_unauthorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }
        response = self.client.post(
            "/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/78a35135-52e3-4af9-8c32-ea3f557354fd/citations/label/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_membershp_contactdetail_citation_authorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            "/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/78a35135-52e3-4af9-8c32-ea3f557354fd/citations/label/",
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_membership_contactdetail_citation_unauthorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }
        response = self.client.put(
            "/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/78a35135-52e3-4af9-8c32-ea3f557354fd/citations/label/09681352a2df465abe59d241b8693f07",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_membership_contactdetail_citation_authorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/78a35135-52e3-4af9-8c32-ea3f557354fd/citations/label/09681352a2df465abe59d241b8693f07",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_membership_contactdetail_citation_unauthorized(self):
        response = self.client.delete(
            "/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/78a35135-52e3-4af9-8c32-ea3f557354fd/citations/label/09681352a2df465abe59d241b8693f07"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_membership_contactdetail_citation_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/memberships/b351cdc2-6961-4fc7-9d61-08fca66e1d44/contact_details/78a35135-52e3-4af9-8c32-ea3f557354fd/citations/label/09681352a2df465abe59d241b8693f07"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)