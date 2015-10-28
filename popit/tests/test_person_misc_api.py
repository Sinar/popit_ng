__author__ = 'sweemeng'
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from popit.models import Person


class PersonLinkAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

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

    def test_view_person_othername_details_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

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

    def test_delete_person_othername_unauthorized(self):
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_othername_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PersonIdentifierAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

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

    def test_view_person_identifier_detail_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["identifier"], "53110321")

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

    def test_delete_person_identifier_unauthorized(self):
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_identifier_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PersonContactAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    def test_view_person_contact_list_unauthorized(self):
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/contacts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["value"], "0123421221")

    def test_view_person_contact_list_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/contacts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["value"], "0123421221")

    def test_view_person_contact_detail_unauthorized(self):
        response = self.client.get(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contacts/a66cb422-eec3-4861-bae1-a64ae5dbde61/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["value"], "0123421221")

    def test_view_person_contact_detail_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contacts/a66cb422-eec3-4861-bae1-a64ae5dbde61/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["value"], "0123421221")

    def test_create_person_contact_unauthorized(self):
        data = {
            "type":"twitter",
            "value": "sinarproject",
        }

        request = self.client.post(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/contacts/",
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
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/contacts/",
            data
        )
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        person_ = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        contact = person_.contacts.language('en').get(type="twitter")
        self.assertEqual(contact.value, "sinarproject")

    def test_update_person_contact_unauthorized(self):
        data = {

            "value": "0123421222",
        }

        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        request = self.client.put(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contacts/a66cb422-eec3-4861-bae1-a64ae5dbde61/",
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
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contacts/a66cb422-eec3-4861-bae1-a64ae5dbde61/",
            data
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        contact = person.contacts.language('en').get(id="a66cb422-eec3-4861-bae1-a64ae5dbde61")
        self.assertEqual(contact.value, "0123421222")

    def test_delete_person_contact_unauthorized(self):
        request = self.client.delete(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contacts/a66cb422-eec3-4861-bae1-a64ae5dbde61/"
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_paerson_contact_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        request = self.client.delete(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contacts/a66cb422-eec3-4861-bae1-a64ae5dbde61/"
        )
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)


# We going to use existing serilaizer.
class PersonNestedAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    def test_get_nested_link_list_unauthorized(self):
        # identifier af7c01b5-1c4f-4c08-9174-3de5ff270bdb
        # link 9c9a2093-c3eb-4b51-b869-0d3b4ab281fd
        # person 8497ba86-7485-42d2-9596-2ab14520f1f4

        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data[0]
        self.assertEqual(data["url"], "http://github.com/sinarproject/")

    def test_get_nested_link_list_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data[0]
        self.assertEqual(data["url"], "http://github.com/sinarproject/")

    def test_get_nested_link_detail_unauthorized(self):
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/9c9a2093-c3eb-4b51-b869-0d3b4ab281fd/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data["url"], "http://github.com/sinarproject/")

    def test_get_nested_link_detail_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/9c9a2093-c3eb-4b51-b869-0d3b4ab281fd/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["url"], "http://github.com/sinarproject/")

    def test_create_nested_link_unauthorized(self):
        data = {
            "url": "http://twitter.com/sinarproject"
        }
        response = self.client.post(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_nested_link_authorized(self):
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

    def test_update_nested_link_unauthorized(self):
        data = {
            "note":"This is a nested link"
        }
        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/9c9a2093-c3eb-4b51-b869-0d3b4ab281fd/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_nested_link_auhtorized(self):
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

    def test_delete_nested_link_unauthorized(self):
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/9c9a2093-c3eb-4b51-b869-0d3b4ab281fd/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_nested_link_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/af7c01b5-1c4f-4c08-9174-3de5ff270bdb/links/9c9a2093-c3eb-4b51-b869-0d3b4ab281fd/"
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)