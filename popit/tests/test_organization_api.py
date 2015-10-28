__author__ = 'sweemeng'
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from popit.models import Organization
from rest_framework import status
from rest_framework.authtoken.models import Token


class OrganizationAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_view_organization_list(self):
        response = self.client.get("/en/organizations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_organization_list_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get("/en/organizations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_organization_detail(self):
        response = self.client.get("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_organization_detail_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_organization_unauthorized(self):
        data = {
            "name": "acme corp"
        }
        response = self.client.post("/en/organizations/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_organization_authorized(self):
        data = {
            "name": "acme corp"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/organizations/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        organization = Organization.objects.language("en").get(name="acme corp")
        self.assertEqual(organization.name, "acme corp")

    def test_update_organization_unauthorized(self):
        data = {
            "abstract": "KL Branch of Pirate Party Malaysia"
        }
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_authorized(self):
        data = {
            "abstract": "KL Branch of Pirate Party Malaysia"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        self.assertEqual(organization.abstract, "KL Branch of Pirate Party Malaysia")

    def test_create_organization_othername_unauthorized(self):
        data = {
            "other_names":[
                {
                    "name": "Not FSociety"
                }
            ]
        }
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_organization_othername_authorized(self):
        data = {
            "other_names":[
                {
                    "name": "Not FSociety"
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        other_name = organization.other_names.language("en").get(name="Not FSociety")
        self.assertEqual(other_name.name, "Not FSociety")

    def test_update_organization_othername_unauthorized(self):
        data = {
            "other_names": [
                {
                    "id" : "53a22b00-1383-4bf5-b4be-4753d8d16062",
                    "note" : "Other Name of Pirate Party"
                }
            ]
        }

        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_othername_authorized(self):
        data = {
            "other_names": [
                {
                    "id" : "53a22b00-1383-4bf5-b4be-4753d8d16062",
                    "note" : "Other Name of Pirate Party"
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        other_name = organization.other_names.language("en").get(id="53a22b00-1383-4bf5-b4be-4753d8d16062")
        self.assertEqual(other_name.note, "Other Name of Pirate Party")

    def test_create_organization_contact_unauthorized(self):
        data = {
            "contacts": [
                {
                    "type": "phone",
                    "value": "01234567",
                    "label": "myphone",
                    "note": "my phone",
                    "valid_from": "2015-01-01",
                    "valid_until": "2020-01-01",
                }
            ]
        }
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_organization_contact_authorized(self):
        data = {
            "contacts": [
                {
                    "type": "phone",
                    "value": "01234567",
                    "label": "myphone",
                    "note": "my phone",
                    "valid_from": "2015-01-01",
                    "valid_until": "2020-01-01",
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        contact = organization.contacts.language("en").get(label="myphone")
        self.assertEqual(contact.value, "01234567")

    def test_update_organization_contact_unauthorized(self):
        data = {
            "contacts": [
                {
                    "id": "651da7cd-f109-4aaa-b04c-df835fb6831f",
                    "value": "01291231321"
                }
            ]
        }
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_contact_authorized(self):
        data = {
            "contacts": [
                {
                    "id": "651da7cd-f109-4aaa-b04c-df835fb6831f",
                    "value": "01291231321"
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        contact = organization.contacts.language("en").get(id="651da7cd-f109-4aaa-b04c-df835fb6831f")
        self.assertEqual(contact.value, "01291231321")

    def test_create_organization_identifier_unauthorized(self):
        data = {
            "identifiers": [
                {
                    "scheme": "testing",
                    "identifier": "12319021390"
                }
            ]
        }
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_organization_identifier_authorized(self):
        data = {
            "identifiers": [
                {
                    "scheme": "testing",
                    "identifier": "12319021390"
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        identifier = organization.identifiers.language("en").get(identifier="12319021390")
        self.assertEqual(identifier.scheme, "testing")

    def test_update_organization_identifier_unauthroized(self):
        data = {
            "identifiers": [
                {
                    "id": "2d3b8d2c-77b8-42f5-ac62-3e83d4408bda",
                    "identifier": "3131313"
                }
            ]
        }

        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_identifier_authorized(self):
        data = {
            "identifiers": [
                {
                    "id": "2d3b8d2c-77b8-42f5-ac62-3e83d4408bda",
                    "identifier": "3131313"
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        identifier = organization.identifiers.language("en").get(id="2d3b8d2c-77b8-42f5-ac62-3e83d4408bda")
        self.assertEqual(identifier.identifier, "3131313")

    def test_create_organization_links_unauthorized(self):
        data = {
            "links": [
                {
                    "url": "http://google.com",
                    "note": "Just a link"
                }
            ]
        }
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_organization_links_authorized(self):
        data = {
            "links": [
                {
                    "url": "http://google.com",
                    "note": "Just a link"
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        link = organization.links.language("en").get(url="http://google.com")
        self.assertEqual(link.note, "Just a link")

    def test_update_organization_link_unauthorized(self):
        data = {
            "links": [
                {
                    "id": "45b0a790-8c9e-4553-844b-431ed34b6b12",
                    "note": "github page of our member"
                }
            ]
        }
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_link_authorized(self):
        data = {
            "links": [
                {
                    "id": "45b0a790-8c9e-4553-844b-431ed34b6b12",
                    "note": "github page of our member"
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")

        link = organization.links.language("en").get(id="45b0a790-8c9e-4553-844b-431ed34b6b12")
        self.assertEqual(link.note, "github page of our member")

    def test_create_nested_link_organization_othername_unauthorized(self):
        data = {
            "other_names": [
                {
                    "id" : "53a22b00-1383-4bf5-b4be-4753d8d16062",
                    "links": [
                        {
                            "url": "http://google.com",
                        }
                    ]
                }
            ]
        }

        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_nested_link_organization_othername_authorized(self):
        data = {
            "other_names": [
                {
                    "id" : "53a22b00-1383-4bf5-b4be-4753d8d16062",
                    "links": [
                        {
                            "url": "http://google.com",
                        }
                    ]
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        other_name = organization.other_names.language("en").get(id="53a22b00-1383-4bf5-b4be-4753d8d16062")
        link = other_name.links.language("en").get(url="http://google.com")
        self.assertEqual(link.url, "http://google.com")

    def test_update_nested_link_organization_othername_unauthorized(self):
        data = {
            "other_names": [
                {
                    "id" : "53a22b00-1383-4bf5-b4be-4753d8d16062",
                    "links": [
                        {
                            "id": "fe662497-c24d-4bbb-a72d-feb77319782a",
                            "note": "Just a link"
                        }
                    ]
                }
            ]
        }

        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_nested_link_organization_othername_authorized(self):
        data = {
            "other_names": [
                {
                    "id" : "53a22b00-1383-4bf5-b4be-4753d8d16062",
                    "links": [
                        {
                            "id": "fe662497-c24d-4bbb-a72d-feb77319782a",
                            "note": "Just a link"
                        }
                    ]
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        other_name = organization.other_names.language("en").get(id="53a22b00-1383-4bf5-b4be-4753d8d16062")
        link = other_name.links.language("en").get(id="fe662497-c24d-4bbb-a72d-feb77319782a")
        self.assertEqual(link.note, "Just a link")
        self.assertEqual(link.field, "name")

    def test_create_nested_link_organization_contact_unauthorized(self):
        data = {
            "contacts": [
                {
                    "id": "651da7cd-f109-4aaa-b04c-df835fb6831f",
                    "links": [
                        {
                            "url": "http://google.com"
                        }
                    ]
                }
            ]
        }
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_nested_link_organization_contact_authorized(self):
        data = {
            "contacts": [
                {
                    "id": "651da7cd-f109-4aaa-b04c-df835fb6831f",
                    "links": [
                        {
                            "url": "http://google.com"
                        }
                    ]
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        contact = organization.contacts.language("en").get(id="651da7cd-f109-4aaa-b04c-df835fb6831f")
        link = contact.links.language("en").get(url="http://google.com")
        self.assertEqual(link.url, "http://google.com")

    def test_update_nested_link_organization_contact_unauthorized(self):
        data = {
            "contacts": [
                {
                    "id": "651da7cd-f109-4aaa-b04c-df835fb6831f",
                    "links": [
                        {
                            "id":"26b8aa4b-2011-493d-bd74-e5e2d6ccd7cf",
                            "note": "yet another link"
                        }
                    ]
                }
            ]
        }

        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_nested_link_organization_contact_authorized(self):
        data = {
            "contacts": [
                {
                    "id": "651da7cd-f109-4aaa-b04c-df835fb6831f",
                    "links": [
                        {
                            "id":"26b8aa4b-2011-493d-bd74-e5e2d6ccd7cf",
                            "note": "yet another link"
                        }
                    ]
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        contact = organization.contacts.language("en").get(id="651da7cd-f109-4aaa-b04c-df835fb6831f")
        link = contact.links.language("en").get(id="26b8aa4b-2011-493d-bd74-e5e2d6ccd7cf")
        self.assertEqual(link.note, "yet another link")

    def test_create_nested_link_organization_identifier_unauthorized(self):
        data = {

            "identifiers": [
                {
                    "id": "2d3b8d2c-77b8-42f5-ac62-3e83d4408bda",
                    "links": [
                        {
                            "url": "http://google.com"
                        }
                    ]
                }
            ]
        }

        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_nested_link_organization_identifier_authorized(self):
        data = {

            "identifiers": [
                {
                    "id": "2d3b8d2c-77b8-42f5-ac62-3e83d4408bda",
                    "links": [
                        {
                            "url": "http://google.com"
                        }
                    ]
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        identifier = organization.identifiers.language("en").get(id="2d3b8d2c-77b8-42f5-ac62-3e83d4408bda")
        link = identifier.links.language("en").get(url="http://google.com")
        self.assertEqual(link.url, "http://google.com")

    def test_update_nested_link_organization_identifier_unauthorized(self):
        data = {

            "identifiers": [
                {
                    "id": "2d3b8d2c-77b8-42f5-ac62-3e83d4408bda",
                    "links": [
                        {
                            "id": "02369098-7b46-4d62-9318-a5f1c2d385bd",
                            "note": "Just a link",

                        }
                    ]
                }
            ]
        }

        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_nested_link_organization_identifier_authorized(self):
        data = {

            "identifiers": [
                {
                    "id": "2d3b8d2c-77b8-42f5-ac62-3e83d4408bda",
                    "links": [
                        {
                            "id": "02369098-7b46-4d62-9318-a5f1c2d385bd",
                            "note": "Just a link",

                        }
                    ]
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        identifier = organization.identifiers.language("en").get(id="2d3b8d2c-77b8-42f5-ac62-3e83d4408bda")
        link = identifier.links.language("en").get(id="02369098-7b46-4d62-9318-a5f1c2d385bd")
        self.assertEqual(link.note, "Just a link")