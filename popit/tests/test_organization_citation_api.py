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


class OrganizationOtherNameCitationAPITestCase(APITestCase):
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

    def test_fetch_organization_othername_field_citation(self):
        response = self.client.get(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/citations"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_organization_othername_citation_list(self):
        response = self.client.get(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/citations/name"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_organization_othername_citation_detail(self):
        response = self.client.get(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/citations/name/63ae5e5b88a4452b81488750be62e0c7/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_organization_othername_citation_unauthorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }

        response = self.client.post(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/citations/name/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_organization_othername_citation_authorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/citations/name/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_organization_othername_citation_unauthorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }

        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/citations/name/63ae5e5b88a4452b81488750be62e0c7/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_othername_citation_authorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/citations/name/63ae5e5b88a4452b81488750be62e0c7/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_organization_othername_citation_unauthorized(self):
        response = self.client.delete(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/citations/name/63ae5e5b88a4452b81488750be62e0c7/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_organization_othername_citation_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/othernames/53a22b00-1383-4bf5-b4be-4753d8d16062/citations/name/63ae5e5b88a4452b81488750be62e0c7/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OrganizationIdentifierCitationAPITestCase(APITestCase):
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

    def test_fetch_organization_identifier_field_citation(self):
        response = self.client.get(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/citations/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_organization_identifier_citation_list(self):
        response = self.client.get(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/citations/identifier/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_organization_identifier_citation_detail(self):
        response = self.client.get(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/citations/identifier/02369098-7b46-4d62-9318-a5f1c2d385bd/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_organization_identifier_citation_unauthorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }

        response = self.client.post(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/citations/identifier/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_organization_identifier_citation_authorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/citations/identifier/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_organization_identifier_citation_unauthorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }
        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/citations/identifier/02369098-7b46-4d62-9318-a5f1c2d385bd/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_identifier_citation_authorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/citations/identifier/02369098-7b46-4d62-9318-a5f1c2d385bd/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_organization_identifier_citation_unauthorized(self):
        response = self.client.delete(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/citations/identifier/02369098-7b46-4d62-9318-a5f1c2d385bd/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_organization_identifier_citation_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/identifiers/2d3b8d2c-77b8-42f5-ac62-3e83d4408bda/citations/identifier/02369098-7b46-4d62-9318-a5f1c2d385bd/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class OrganizationContactDetailCitationAPITestCase(APITestCase):
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

    def test_fetch_organization_contactdetails_field_citation(self):
        response = self.client.get(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/citations/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_organization_contactdetails_citation_list(self):
        response = self.client.get(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/citations/label/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_organization_conttactdetails_citation_details(self):
        response = self.client.get(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/citations/label/1a046be50da9448a970c940927732005"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_organization_contactdetails_citation_unauthorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }
        response = self.client.post(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/citations/label/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_organization_contactdetails_citation_authorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/citations/label/",
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_organization_contactdetails_citation_unauthorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }

        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/citations/label/1a046be50da9448a970c940927732005",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_organization_contactdetails_citation_authorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/citations/label/1a046be50da9448a970c940927732005",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_organization_contactdetails_citation_unauthorized(self):
        response = self.client.delete(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/citations/label/1a046be50da9448a970c940927732005"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_organization_contactdetails_citation_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete(
            "/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/contact_details/651da7cd-f109-4aaa-b04c-df835fb6831f/citations/label/1a046be50da9448a970c940927732005"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)