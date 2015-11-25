__author__ = 'sweemeng'
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from popit.models import Person
from popit.signals.handlers import *
from popit.models import *


class PersonLinkAPITestCase(APITestCase):

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

    def test_view_person_link_list_unauthorized(self):
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/links/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_person_link_list_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/links/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_person_link_details_unauthorized(self):
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/links/a4ffa24a9ef3cbcb8cfaa178c9329367/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_person_link_details_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/links/a4ffa24a9ef3cbcb8cfaa178c9329367/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_person_link_details_not_exist_unauthorized(self):
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_person_link_details_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_person_links_unauthorized(self):
        data = {
            "url": "http://twitter.com/sweemeng",
        }
        response = self.client.post("/en/persons/ab1a5788e5bae955c048748fa6af0e97/links/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_person_links_authorized(self):
        data = {
            "url": "http://twitter.com/sweemeng",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/persons/ab1a5788e5bae955c048748fa6af0e97/links/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        url = person_.links.language("en").get(url="http://twitter.com/sweemeng")
        self.assertEqual(url.url, "http://twitter.com/sweemeng")

    def test_update_person_links_unauthorized(self):
        data = {
            "note": "just a random repo"
        }
        response = self.client.put(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/links/a4ffa24a9ef3cbcb8cfaa178c9329367/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_links_not_exist_unauthorized(self):
        data = {
            "note": "just a random repo"
        }
        response = self.client.put(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/links/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_links_authorized(self):
        data = {
            "note": "just a random repo"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/links/a4ffa24a9ef3cbcb8cfaa178c9329367/",
            data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        url = person.links.language("en").get(id="a4ffa24a9ef3cbcb8cfaa178c9329367")
        self.assertEqual(url.note, "just a random repo")

    def test_update_person_links_not_exist_authorized(self):
        data = {
            "note": "just a random repo"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/links/not_exist/",
            data
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_person_links_unauthorized(self):
        response = self.client.delete("/en/persons/ab1a5788e5bae955c048748fa6af0e97/links/a4ffa24a9ef3cbcb8cfaa178c9329367/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_links_not_exist_unauthorized(self):
        response = self.client.delete("/en/persons/ab1a5788e5bae955c048748fa6af0e97/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_links_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/persons/ab1a5788e5bae955c048748fa6af0e97/links/a4ffa24a9ef3cbcb8cfaa178c9329367/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_person_links_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/persons/ab1a5788e5bae955c048748fa6af0e97/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PersonOtherNameAPITestCase(APITestCase):

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

    def test_view_person_othername_list_unauthorized(self):
        response = self.client.get("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_person_othername_list_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_person_othername_details_unauthorized(self):
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_person_othername_details_not_exist_unauthorized(self):
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_person_othername_details_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_person_othername_details_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_person_othername_unauthorized(self):
        data = {
            "name": "jane",
            "family_name": "jambul",
            "given_name": "test person",
            "start_date": "1950-01-01",
            "end_date": "2010-01-01",
        }
        response = self.client.post(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/", data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_person_othername_authorized(self):
        data = {
            "name": "jane",
            "family_name": "jambul",
            "given_name": "test person",
            "start_date": "1950-01-01",
            "end_date": "2010-01-01",
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/othernames/", data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        other_name = person_.other_names.language('en').get(name="jane")
        self.assertEqual(other_name.given_name, "test person")

    def test_update_person_othername_unauthorized(self):
        data = {
            "family_name": "jambul",
        }
        person = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        other_name = person.other_names.language('en').get(id="cf93e73f-91b6-4fad-bf76-0782c80297a8")
        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_othername_not_exist_unauthorized(self):
        data = {
            "family_name": "jambul",
        }

        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_update_person_othername_authorized(self):
        data = {
            "family_name": "jambul",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        person = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        other_name = person.other_names.language('en').get(id="cf93e73f-91b6-4fad-bf76-0782c80297a8")
        self.assertEqual(other_name.family_name, "jambul")

    def test_update_person_othername_not_exist_authorized(self):
        data = {
            "family_name": "jambul",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_person_othername_unauthorized(self):
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_othername_not_exist_unauthorized(self):
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_othername_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_person_othername_not_exist_authorized(self):

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PersonIdentifierAPITestCase(APITestCase):

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

    def test_view_person_identifier_list_unauthorized(self):
        response = self.client.get("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_person_identifier_list_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_person_identifier_detail_unauthorized(self):
        response = self.client.get("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["identifier"], "53110321")

    def test_view_person_identifier_detail_not_exist_unauthorized(self):
        response = self.client.get("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_person_identifier_detail_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["identifier"], "53110321")

    def test_view_person_identifier_detail_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_person_identifier_unauthorized(self):
        data = {
            "scheme": "IC",
            "identifier": "129031309",
        }
        response = self.client.post("/en/persons/ab1a5788e5bae955c048748fa6af0e97/identifiers/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_person_identifier_authorized(self):
        data = {
            "scheme": "IC",
            "identifier": "129031309",
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/persons/ab1a5788e5bae955c048748fa6af0e97/identifiers/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        person = Person.objects.language("en").get(id="ab1a5788e5bae955c048748fa6af0e97")
        identifier = person.identifiers.language("en").get(identifier="129031309")
        self.assertEqual(identifier.scheme, "IC")

    def test_update_person_identifier_unauthorized(self):
        data = {
            "identifier": "53110322",
        }
        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_identifier_not_exist_unauthorized(self):
        data = {
            "identifier": "53110322",
        }
        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_identifier_authorized(self):
        data = {
            "identifier": "53110322",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/",
            data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        person_ = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        identifier = person_.identifiers.language('en').get(id="34b59cb9-607a-43c7-9d13-dfe258790ebf")
        self.assertEqual(identifier.identifier, '53110322')

    def test_update_person_identifier_not_exist_authorized(self):
        data = {
            "identifier": "53110322",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/not_exist/",
            data
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_person_identifier_unauthorized(self):
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_identifer_not_exist_unauthorized(self):
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_identifier_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_person_identifier_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PersonContactAPITestCase(APITestCase):

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

    def test_view_person_contact_list_unauthorized(self):
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["value"], "0123421221")

    def test_view_person_contact_list_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["value"], "0123421221")

    def test_view_person_contact_detail_unauthorized(self):
        response = self.client.get(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["value"], "0123421221")

    def test_view_person_contact_detail_not_exist_unauthorized(self):
        response = self.client.get(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_person_contact_detail_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["value"], "0123421221")

    def test_view_person_contact_detail_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_person_contact_unauthorized(self):
        data = {
            "type":"twitter",
            "value": "sinarproject",
        }

        request = self.client.post(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/contact_details/",
            data
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_person_contact_authorized(self):
        data = {
            "type":"twitter",
            "value": "sinarproject",
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        request = self.client.post(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/contact_details/",
            data
        )
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        person_ = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        contact = person_.contact_details.language('en').get(type="twitter")
        self.assertEqual(contact.value, "sinarproject")

    def test_update_person_contact_unauthorized(self):
        data = {

            "value": "0123421222",
        }

        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        request = self.client.put(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/",
            data
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_contact_not_exist_unauthorized(self):
        data = {

            "value": "0123421222",
        }

        request = self.client.put(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/not_exist/",
            data
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_contact_authorized(self):
        data = {

            "value": "0123421222",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        request = self.client.put(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/",
            data
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        contact = person.contact_details.language('en').get(id="a66cb422-eec3-4861-bae1-a64ae5dbde61")
        self.assertEqual(contact.value, "0123421222")

    def test_update_person_contact_not_exist_authorized(self):
        data = {

            "value": "0123421222",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        request = self.client.put(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/not_exist/",
            data
        )
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_person_contact_unauthorized(self):
        request = self.client.delete(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/"
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_contact_not_exist_unauthorized(self):
        request = self.client.delete(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/not_exist/"
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_contact_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        request = self.client.delete(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/"
        )
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_person_contact_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        request = self.client.delete(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/not_exist/"
        )
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)


# We going to use existing serilaizer.
class PersonIdentifierLinkAPITestCase(APITestCase):

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

    def test_get_person_identifier_link_list_unauthorized(self):
        # identifier af7c01b5-1c4f-4c08-9174-3de5ff270bdb
        # link 9c9a2093-c3eb-4b51-b869-0d3b4ab281fd
        # person 8497ba86-7485-42d2-9596-2ab14520f1f4

        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data[0]
        self.assertEqual(data["url"], "http://github.com/sinarproject/")

    def test_get_person_identifier_link_list_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data[0]
        self.assertEqual(data["url"], "http://github.com/sinarproject/")

    def test_get_person_identifier_link_detail_unauthorized(self):
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/9c9a2093-c3eb-4b51-b869-0d3b4ab281fd/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["url"], "http://github.com/sinarproject/")

    def test_get_person_identifier_link_detail_not_exist_unauthorized(self):
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_person_identifier_link_detail_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/9c9a2093-c3eb-4b51-b869-0d3b4ab281fd/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["url"], "http://github.com/sinarproject/")

    def test_get_person_identifier_link_detail_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_person_identifier_link_unauthorized(self):
        data = {
            "url": "http://twitter.com/sinarproject"
        }
        response = self.client.post(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_person_identifier_link_authorized(self):
        data = {
            "url": "http://twitter.com/sinarproject"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        identifier = person.identifiers.language("en").get(id="af7c01b5-1c4f-4c08-9174-3de5ff270bdb")
        link = identifier.links.language("en").get(url="http://twitter.com/sinarproject")
        self.assertEqual(link.url, "http://twitter.com/sinarproject")

    def test_update_person_identifier_link_unauthorized(self):
        data = {
            "note":"This is a nested link"
        }
        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/9c9a2093-c3eb-4b51-b869-0d3b4ab281fd/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_identifier_link_not_exist_unauthorized(self):
        data = {
            "note":"This is a nested link"
        }
        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_identifier_link_authorized(self):
        data = {
            "note":"This is a nested link"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/9c9a2093-c3eb-4b51-b869-0d3b4ab281fd/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 9c9a2093-c3eb-4b51-b869-0d3b4ab281fd
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        identifier = person.identifiers.language("en").get(id="af7c01b5-1c4f-4c08-9174-3de5ff270bdb")
        link = identifier.links.language("en").get(id="9c9a2093-c3eb-4b51-b869-0d3b4ab281fd")
        self.assertEqual(link.note, "This is a nested link")

    def test_update_person_identifier_link_not_exist_authorized(self):
        data = {
            "note":"This is a nested link"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_person_identifier_link_unauthorized(self):
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/9c9a2093-c3eb-4b51-b869-0d3b4ab281fd/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_identifier_link_not_exist_unauthorized(self):
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_identifier_link_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/9c9a2093-c3eb-4b51-b869-0d3b4ab281fd/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_person_identifier_link_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/not_exist/"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PersonOtherNameLinkAPITestCase(APITestCase):

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

    def test_list_person_othername_link(self):
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/links/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_person_othername_link_detail_not_exist(self):
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/links/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_show_person_othername_link_detail(self):
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/links/4d8d71c4-20ea-4ed1-ae38-4b7d7550cdf6/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_person_othername_link_unauthorized(self):
        data = {
            "url": "http://github.com/sinar"
        }

        response = self.client.post(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/links/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_person_othername_link_authorized(self):
        data = {
            "url": "http://github.com/sinar"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/links/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_person_othername_link_not_exist_unauthorized(self):
        data = {
            "note": "Just a link"
        }

        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/links/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_othername_link_not_exist_authorized(self):
        data = {
            "note": "Just a link"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/links/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_person_othername_link_unauthorized(self):
        data = {
            "note": "Just a link"
        }

        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/links/4d8d71c4-20ea-4ed1-ae38-4b7d7550cdf6/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_othername_link_authorized(self):
        data = {
            "note": "Just a link"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/links/4d8d71c4-20ea-4ed1-ae38-4b7d7550cdf6/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_person_othername_link_not_exist_unauthorized(self):
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/links/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_othername_link_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/links/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_person_othername_link_unauthorized(self):
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/links/4d8d71c4-20ea-4ed1-ae38-4b7d7550cdf6/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_othername_link_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/links/4d8d71c4-20ea-4ed1-ae38-4b7d7550cdf6/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PersonContactLinkAPITestCase(APITestCase):

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

    def test_list_person_contact_link(self):
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/contact_details/2256ec04-2d1d-4994-b1f1-16d3f5245441/links/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_person_contact_link_not_exist(self):
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/contact_details/2256ec04-2d1d-4994-b1f1-16d3f5245441/links/not_exist/"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_show_person_contact_link(self):
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/contact_details/2256ec04-2d1d-4994-b1f1-16d3f5245441/links/6d0afb46-67d4-4708-87c4-4d51ce99767e/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_person_contact_link_unauthorized(self):
        data = {
            "url": "http://github.com/sinar"
        }

        response = self.client.post(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/contact_details/2256ec04-2d1d-4994-b1f1-16d3f5245441/links/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_person_contact_link_authorized(self):
        data = {
            "url": "http://github.com/sinar"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/contact_details/2256ec04-2d1d-4994-b1f1-16d3f5245441/links/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_person_contact_link_not_exist_unauthorized(self):
        data = {
            "note": "Just a link"
        }

        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/contact_details/2256ec04-2d1d-4994-b1f1-16d3f5245441/links/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_contact_link_not_exist_authorized(self):
        data = {
            "note": "Just a link"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/contact_details/2256ec04-2d1d-4994-b1f1-16d3f5245441/links/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_person_contact_link_unauthorized(self):
        data = {
            "note": "Just a link"
        }

        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/contact_details/2256ec04-2d1d-4994-b1f1-16d3f5245441/links/6d0afb46-67d4-4708-87c4-4d51ce99767e/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_contact_link_authorized(self):
        data = {
            "note": "Just a link"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/contact_details/2256ec04-2d1d-4994-b1f1-16d3f5245441/links/6d0afb46-67d4-4708-87c4-4d51ce99767e/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_person_contact_link_not_exist_unauthorized(self):
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/contact_details/2256ec04-2d1d-4994-b1f1-16d3f5245441/links/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_contact_link_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/contact_details/2256ec04-2d1d-4994-b1f1-16d3f5245441/links/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_person_contact_link_unauthorized(self):
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/contact_details/2256ec04-2d1d-4994-b1f1-16d3f5245441/links/6d0afb46-67d4-4708-87c4-4d51ce99767e/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_contact_link_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/contact_details/2256ec04-2d1d-4994-b1f1-16d3f5245441/links/6d0afb46-67d4-4708-87c4-4d51ce99767e/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)