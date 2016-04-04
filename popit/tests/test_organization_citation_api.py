from rest_framework.test import APITestCase
from popit.signals.handlers import *
from popit.models import *
from rest_framework import status


class OrganizationCitationAPITestCase(APITestCase):
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

    def test_fetch_organization_field_citations(self):
        requests = self.client.get(
            "/en/organizations/612943b1-864d-4188-8d79-ca387ed19b32/citations/"
        )
        self.assertEqual(requests.status_code, status.HTTP_200_OK)

    def test_fetch_organization_citations_list(self):
        requests = self.client.get(
            "/en/organizations/612943b1-864d-4188-8d79-ca387ed19b32/citations/name/"
        )
        self.assertEqual(requests.status_code, status.HTTP_200_OK)

    def test_fetch_organization_citations_detail(self):
        requests = self.client.get(
            "/en/organizations/612943b1-864d-4188-8d79-ca387ed19b32/citations/name/a9978227d40a4decb2fdc6387e085753/"
        )
        self.assertEqual(requests.status_code, status.HTTP_200_OK)

    def test_create_organization_citation_unauthorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }
        request = self.client.post(
            "/en/organizations/612943b1-864d-4188-8d79-ca387ed19b32/citations/name/",
            data=data
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_organization_citation_authorizes(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(
            "/en/organizations/612943b1-864d-4188-8d79-ca387ed19b32/citations/name/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_organization_citation_unauthorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }
        response = self.client.put(
            "/en/organizations/612943b1-864d-4188-8d79-ca387ed19b32/citations/name/a9978227d40a4decb2fdc6387e085753/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_citation_authorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/organizations/612943b1-864d-4188-8d79-ca387ed19b32/citations/name/a9978227d40a4decb2fdc6387e085753/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_organization_citation_unauthorized(self):
        response = self.client.delete(
            "/en/organizations/612943b1-864d-4188-8d79-ca387ed19b32/citations/name/a9978227d40a4decb2fdc6387e085753/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_organization_citation_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete(
            "/en/organizations/612943b1-864d-4188-8d79-ca387ed19b32/citations/name/a9978227d40a4decb2fdc6387e085753/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)