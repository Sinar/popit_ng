__author__ = 'sweemeng'
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from popit.models import Organization
from rest_framework import status
from rest_framework.authtoken.models import Token


class OrganizationOtherNameAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    def test_list_organization_othername(self):
        response = self.client.get("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_organization_othername_detail_not_exist(self):
        response = self.client.get(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_show_organization_othername_detail(self):
        response = self.client.get(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_organization_othername_unauthorized(self):
        data = {
            "name": "Not FSociety"
        }
        response = self.client.post("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_organization_othername_authorized(self):
        data = {
            "name": "Not FSociety"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        other_name = organization.other_names.language("en").get(name="Not FSociety")
        self.assertEqual(other_name.name, "Not FSociety")

    def test_update_organization_othername_not_exist_unauthorized(self):
        data = {
            "id" : "53a22b00-1383-4bf5-b4be-4753d8d16062",
            "note" : "Other Name of Pirate Party"
        }
        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_othername_not_exist_authorized(self):
        data = {
            "note" : "Other Name of Pirate Party"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_organization_othername_unauthorized(self):
        data = {
            "note" : "Other Name of Pirate Party"
        }

        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_othername_authorized(self):
        data = {
            "note" : "Other Name of Pirate Party"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        other_name = organization.other_names.language("en").get(id="53a22b00-1383-4bf5-b4be-4753d8d16062")
        self.assertEqual(other_name.note, "Other Name of Pirate Party")

    def test_delete_organization_othername_not_exist_unauthorized(self):
        response = self.client.delete("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_organization_othername_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_organization_othername_unauthorized(self):
        response = self.client.delete("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_organization_othername_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OrganizationContactAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    def test_list_organization_contact(self):
        response = self.client.get("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_organization_contact_not_exist(self):
        response = self.client.get("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_show_organization_contact(self):
        response = self.client.get("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_organization_contact_unauthorized(self):
        data = {
            "type": "phone",
            "value": "01234567",
            "label": "myphone",
            "note": "my phone",
            "valid_from": "2015-01-01",
            "valid_until": "2020-01-01",
        }
        response = self.client.post("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_organization_contact_authorized(self):
        data = {
            "type": "phone",
            "value": "01234567",
            "label": "myphone",
            "note": "my phone",
            "valid_from": "2015-01-01",
            "valid_until": "2020-01-01",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_organization_contact_not_exist_unauthorized(self):
        data = {
            "value": "01291231321"
        }
        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_contact_not_exist_authorized(self):
        data = {
            "value": "01291231321"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_organization_contact_unauthorized(self):
        data = {
            "value": "01291231321"
        }
        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/",
            data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_contact_authorized(self):
        data = {
            "value": "01291231321"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/",
            data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_organization_contact_does_not_exist_unauthorized(self):
        response = self.client.delete("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_organizatioN_contact_does_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_delete_organization_contact_unauthorized(self):

        response = self.client.delete("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_delete_organization_contact_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OrganizationIdentifierAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    def test_list_organization_identifier(self):
        response = self.client.get("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_organization_identifier_not_exist(self):
        response = self.client.get("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/not_exists/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_show_organization_identifier(self):
        response = self.client.get("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_organization_identifier_unauthorized(self):
        data = {
            "scheme": "testing",
            "identifier": "12319021390"
        }
        response = self.client.post("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_organization_identifier_authorized(self):
        data = {
            "scheme": "testing",
            "identifier": "12319021390"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        identifier = organization.identifiers.language("en").get(identifier="12319021390")
        self.assertEqual(identifier.scheme, "testing")

    def test_update_organization_identifier_not_exist_unauthorized(self):
        data = {
            "identifier": "3131313"
        }
        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_identifier_not_exist_authorized(self):
        data = {
            "identifier": "3131313"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_organization_identifier_unauthorized(self):
        data = {
            "identifier": "3131313"
        }
        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/",
            data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_identifier_authorized(self):
        data = {
            "identifier": "3131313"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/",
            data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_organization_identifier_not_exist_unauthorized(self):
        response = self.client.delete("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_organization_identifier_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_organization_identifier_unauthorized(self):
        response = self.client.delete("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_organization_identifier_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OrganizationLinksAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    def test_list_organization_link(self):
        response = self.client.get("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/links/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_organization_link_not_exist(self):
        response = self.client.get("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_show_organization_link(self):
        response = self.client.get("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/links/45b0a790-8c9e-4553-844b-431ed34b6b12/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_organization_link_unauthorized(self):
        data = {
            "url": "http://google.com",
            "note": "Just a link"
        }
        response = self.client.post("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/links/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_organization_link_authorized(self):
        data = {
            "url": "http://google.com",
            "note": "Just a link"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/links/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_organization_link_not_exist_unauthorized(self):
        data = {
            "note": "github page of our member"
        }
        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/links/not_exist",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_link_not_exist_authorized(self):
        data = {
            "note": "github page of our member"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/links/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_organization_link_unauthorized(self):
        data = {
            "note": "github page of our member"
        }
        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/links/45b0a790-8c9e-4553-844b-431ed34b6b12/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_link_authorized(self):
        data = {
            "note": "github page of our member"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/links/45b0a790-8c9e-4553-844b-431ed34b6b12/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_organization_link_not_exist_unauthorized(self):
        response = self.client.delete("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_organization_link_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_organization_link_unauthorized(self):
        response = self.client.delete("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/links/45b0a790-8c9e-4553-844b-431ed34b6b12/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_organization_link_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/links/45b0a790-8c9e-4553-844b-431ed34b6b12/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OrganizationIdentifierLinkAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    def test_list_organization_identifier_link(self):
        response = self.client.get(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/links/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_organization_identifier_link_not_exist(self):
        response = self.client.get(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/links/not_exists/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_show_organization_identifier_link(self):
        response = self.client.get(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/links/02369098-7b46-4d62-9318-a5f1c2d385bd/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_organization_identifier_link_unauthorized(self):
        data = {
            "url": "http://google.com"
        }
        response = self.client.post(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/links/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_organization_identifier_link_authorized(self):
        data = {
            "url": "http://google.com"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/links/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_organization_identifier_link_not_exists_unauthorized(self):
        data = {
            "note": "Just a link",
        }
        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/links/not_exists/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_update_organization_identifier_link_not_exists_authorized(self):
        data = {
            "note": "Just a link",
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/links/not_exists/",
            data
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_organization_identifier_link_unauthorized(self):
        data = {
            "note": "Just a link",
        }

        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/links/02369098-7b46-4d62-9318-a5f1c2d385bd/",
            data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_identifier_link_authorized(self):
        data = {
            "note": "Just a link",
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/links/02369098-7b46-4d62-9318-a5f1c2d385bd/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_organization_identifier_link_not_exist_unauthorized(self):
        response = self.client.delete("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_organization_identifier_link_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_organization_identifier_link_unauthorized(self):
        response = self.client.delete(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/links/02369098-7b46-4d62-9318-a5f1c2d385bd/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_organization_identifier_link_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/links/02369098-7b46-4d62-9318-a5f1c2d385bd/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OrganizationContactLinkAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    def test_list_organization_contact_link(self):
        response = self.client.get(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/links/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_organization_contact_link(self):
        response = self.client.get(
             "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/links/26b8aa4b-2011-493d-bd74-e5e2d6ccd7cf/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_organization_contact_link_not_exist(self):
        response = self.client.get(
             "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/links/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_organization_contact_link_unauthorized(self):
        data = {
            "url": "http://google.com"
        }
        response = self.client.post(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/links/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_organization_contact_link_authorized(self):
        data = {
            "url": "http://google.com"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/links/",
            data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_organization_contact_link_not_exist_unauthorized(self):
        data = {
            "note": "Just a link"
        }

        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/links/not_exists/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_contact_link_not_exist_authorized(self):
        data = {
            "note": "Just a link"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/links/not_exists/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_update_organization_contact_link_unauthorized(self):
        data = {
            "note": "yet another link"
        }

        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/links/26b8aa4b-2011-493d-bd74-e5e2d6ccd7cf/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_contact_link_authorized(self):
        data = {
            "note": "yet another link"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/links/26b8aa4b-2011-493d-bd74-e5e2d6ccd7cf/",
            data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_organization_contact_link_not_exist_unauthorized(self):
        response = self.client.delete(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/links/not_exists/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_organization_contact_link_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/links/not_exists/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_organization_contact_link_unauthorized(self):
        response = self.client.delete(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/links/26b8aa4b-2011-493d-bd74-e5e2d6ccd7cf/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_organization_contact_link_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/links/26b8aa4b-2011-493d-bd74-e5e2d6ccd7cf/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OrganizationOtherNameLinksAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    def test_list_organization_othername_link(self):
        response = self.client.get(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/links/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_organization_othername_link_not_exist(self):
        response = self.client.get(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/links/not_exists/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_show_organization_othername_link(self):
        response = self.client.get(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/links/fe662497-c24d-4bbb-a72d-feb77319782a/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_organization_othername_link_unauthorized(self):
        data = {
            "url": "http://google.com",
        }
        response = self.client.post(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/links/",
            data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_organization_othername_link_authorized(self):
        data = {
            "url": "http://google.com",
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/links/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_organization_othername_link_not_exist_unauthorized(self):
        data = {
            "note": "Just a link"
        }

        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/links/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_othername_link_not_exist_authorized(self):
        data = {
            "note": "Just a link"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/links/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_organization_othername_link_unauthorized(self):
        data = {
            "id": "fe662497-c24d-4bbb-a72d-feb77319782a",
            "note": "Just a link"
        }

        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/links/fe662497-c24d-4bbb-a72d-feb77319782a/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_othername_link_authorized(self):
        data = {
            "note": "Just a link"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/links/fe662497-c24d-4bbb-a72d-feb77319782a/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_organization_othername_link_not_exist_unauthorized(self):
        response = self.client.delete(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/links/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_organization_othername_link_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/links/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_organization_othername_link_unauthorized(self):
        response = self.client.delete(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/links/fe662497-c24d-4bbb-a72d-feb77319782a/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_organization_othername_link_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/links/fe662497-c24d-4bbb-a72d-feb77319782a/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)