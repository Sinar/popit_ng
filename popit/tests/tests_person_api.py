__author__ = 'sweemeng'
from rest_framework.test import APITestCase
from django.test import TestCase
from popit.models import Person
from popit.serializers import PersonSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from popit.signals.handlers import *
from popit.models import *


# TODO: Test multilingual behavior. To make behavior clear
# TODO: Need new fixtures
class PersonSerializerTestCase(TestCase):
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

    def test_fetch_non_empty_field_person_serializer(self):
        person = Person.objects.untranslated().get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        serializer = PersonSerializer(person, language='en')
        data = serializer.data
        self.assertEqual(data["name"], "John")

    def test_fetch_empty_field_person_serializer(self):
        person = Person.objects.untranslated().get(id='ab1a5788e5bae955c048748fa6af0e97')
        serializer = PersonSerializer(person, language='en')
        data = serializer.data
        self.assertEqual(data["given_name"], "")

    def test_fetch_not_empty_relation_person_serializer(self):
        person = Person.objects.untranslated().get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        serializer = PersonSerializer(person, language='en')
        data = serializer.data
        self.assertTrue(data["other_names"])

    def test_fetch_empty_relation_person_serializer(self):
        person = Person.objects.untranslated().get(id='ab1a5788e5bae955c048748fa6af0e97')
        serializer = PersonSerializer(person, language='en')
        data = serializer.data
        self.assertFalse(data["other_names"])

    def test_create_person_with_all_field_serializer(self):

        person_data = {
            "name": "joe",
            "family_name": "doe",
            "given_name": "joe jambul",
            "additional_name": "not john doe",
            "gender": "unknown",
            "summary": "person unit test api",
            "honorific_prefix": "Chief",
            "honorific_suffix": "of the fake people league",
            "biography": "He does not exists!!!!",
            "birth_date": "1950-01-01",
            "death_data": "2000-01-01",
            "email": "joejambul@sinarproject.org",
            "contact_details":[
                {
                    "type":"twitter",
                    "value": "sinarproject",
                }
            ],
            "links":[
                {
                    "url":"http://sinarproject.org",
                }
            ],
            "identifiers":[
                {
                    "identifier": "9089098098",
                    "scheme": "rakyat",
                }
            ],
            "other_names":[
                {
                    "name":"Jane",
                    "family_name":"Jambul",
                    "start_date": "1950-01-01",
                    "end_date": "2010-01-01",
                }
            ]
        }
        person_serial = PersonSerializer(data=person_data, language='en')
        person_serial.is_valid()
        self.assertEqual(person_serial.errors, {})
        person_serial.save()
        person = Person.objects.language("en").get(name="joe")
        self.assertEqual(person.given_name, "joe jambul")

    def test_update_person_serializer(self):
        person_data = {
            "given_name": "jerry jambul",
        }
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')

        person_serializer = PersonSerializer(person, data=person_data, partial=True, language='en')
        person_serializer.is_valid()
        self.assertEqual(person_serializer.errors, {})
        person_serializer.save()
        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        self.assertEqual(person_.given_name, "jerry jambul")

    def test_create_links_person_serializers(self):
        person_data = {
            "links": [
                {
                    "url": "http://twitter.com/sweemeng",
                }
            ]
        }

        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        person_serializer = PersonSerializer(person, data=person_data, partial=True, language='en')
        person_serializer.is_valid()
        self.assertEqual(person_serializer.errors, {})
        person_serializer.save()
        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        url = person_.links.language("en").get(url="http://twitter.com/sweemeng")
        self.assertEqual(url.url, "http://twitter.com/sweemeng")

    def test_update_links_person_serializers(self):
        # links id a4ffa24a9ef3cbcb8cfaa178c9329367
        person_data = {
            "id":"ab1a5788e5bae955c048748fa6af0e97",
            "links":[
                {
                    "id": "a4ffa24a9ef3cbcb8cfaa178c9329367",
                    "note": "just a random repo"
                }
            ]
        }
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        person_serializer = PersonSerializer(person, data=person_data, partial=True)
        person_serializer.is_valid()

        self.assertEqual(person_serializer.errors, {})
        person_serializer.save()
        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        url = person_.links.language("en").get(id="a4ffa24a9ef3cbcb8cfaa178c9329367")
        self.assertEqual(url.note, "just a random repo")

    def test_update_create_nested_links_persons_serializer(self):
        person_data = {
            "id":"ab1a5788e5bae955c048748fa6af0e97",
            "contact_details":[
                {
                    "id": "a66cb422-eec3-4861-bae1-a64ae5dbde61",
                    "links": [{
                        "url": "http://facebook.com",
                    }]
                }
            ],
        }
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        person_serializer = PersonSerializer(person, data=person_data, partial=True, language='en')
        person_serializer.is_valid()
        self.assertEqual(person_serializer.errors, {})
        person_serializer.save()
        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        # There should be only 1 links in that contact
        contact = person_.contact_details.language('en').get(id='a66cb422-eec3-4861-bae1-a64ae5dbde61')
        links = contact.links.language('en').all()
        self.assertEqual(links[0].url, "http://facebook.com")

    def test_update_update_nested_links_person_serializer(self):
        person_data = {
            "id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "identifiers":[
                {
                    "id": "af7c01b5-1c4f-4c08-9174-3de5ff270bdb",
                    "links": [{
                        "id": "9c9a2093-c3eb-4b51-b869-0d3b4ab281fd",
                        "note": "this is just a test note",
                    }]
                }
            ],
        }
        person = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        person_serializer = PersonSerializer(person, data=person_data, partial=True, language='en')
        person_serializer.is_valid()
        self.assertEqual(person_serializer.errors, {})
        person_serializer.save()
        person_ = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        identifier = person_.identifiers.language('en').get(id="af7c01b5-1c4f-4c08-9174-3de5ff270bdb")
        link = identifier.links.language('en').get(id="9c9a2093-c3eb-4b51-b869-0d3b4ab281fd")
        self.assertEqual(link.note, "this is just a test note")

    def test_create_identifier_person_serializer(self):
        person_data = {
            "identifiers": [
                {
                    "scheme": "IC",
                    "identifier": "129031309",
                }
            ]
        }
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        person_serializer = PersonSerializer(person, data=person_data, partial=True, language='en')
        person_serializer.is_valid()
        self.assertEqual(person_serializer.errors, {})
        person_serializer.save()
        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')

        identifier = person_.identifiers.language('en').get(identifier="129031309")
        self.assertEqual(identifier.scheme, "IC")

    def test_update_identifier_person_serializer(self):
        person_data = {
            "identifiers": [
                {
                    "id": "34b59cb9-607a-43c7-9d13-dfe258790ebf",
                    "identifier": "53110322",
                }
            ]
        }

        person = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        person_serializer = PersonSerializer(person, data=person_data, partial=True)
        person_serializer.is_valid()
        self.assertEqual(person_serializer.errors, {})
        person_serializer.save()
        person_ = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        identifier = person_.identifiers.language('en').get(id="34b59cb9-607a-43c7-9d13-dfe258790ebf")
        self.assertEqual(identifier.identifier, '53110322')

    def test_create_contact_person_serializer(self):
        person_data = {
            "contact_details": [
                {
                    "type":"twitter",
                    "value": "sinarproject",
                }
            ]
        }
        person = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        person_serializer = PersonSerializer(person, data=person_data, partial=True, language='en')
        person_serializer.is_valid()
        self.assertEqual(person_serializer.errors, {})
        person_serializer.save()
        person_ = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        contact = person_.contact_details.language('en').get(type="twitter")
        self.assertEqual(contact.value, "sinarproject")

    def test_update_contact_person_serializer(self):
        person_data = {
            "contact_details": [
                {
                    "id": "a66cb422-eec3-4861-bae1-a64ae5dbde61",
                    "value": "0123421222",
                }
            ]
        }
        person = Person.objects.untranslated().get(id='ab1a5788e5bae955c048748fa6af0e97')
        person_serializer = PersonSerializer(person, data=person_data, partial=True, language="en")
        person_serializer.is_valid()
        self.assertEqual(person_serializer.errors, {})
        person_serializer.save()
        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        contact = person_.contact_details.language('en').get(id="a66cb422-eec3-4861-bae1-a64ae5dbde61")
        self.assertEqual(contact.value, "0123421222")

    def test_create_other_name_person_serializer(self):
        person_data = {
            "other_names": [
                {
                    "name": "jane",
                    "family_name": "jambul",
                    "given_name": "test person",
                    "start_date": "1950-01-01",
                    "end_date": "2010-01-01",
                }
            ]
        }
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        person_serializer = PersonSerializer(person, data=person_data, partial=True, language='en')
        person_serializer.is_valid()
        self.assertEqual(person_serializer.errors, {})
        person_serializer.save()
        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        other_name = person_.other_names.language('en').get(name="jane")
        self.assertEqual(other_name.given_name, "test person")

    def test_update_other_person_serializer(self):
        person_data = {
            "other_names": [
                {
                    "id": "cf93e73f-91b6-4fad-bf76-0782c80297a8",
                    "family_name": "jambul",
                }
            ]
        }
        person = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        person_serializer = PersonSerializer(person, data=person_data, partial=True, language='en')
        person_serializer.is_valid()
        self.assertEqual(person_serializer.errors, {})
        person_serializer.save()
        person_ = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        other_name = person_.other_names.language('en').get(id="cf93e73f-91b6-4fad-bf76-0782c80297a8")
        self.assertEqual(other_name.family_name, "jambul")


# TODO: Test with different language url. For integration
# TODO: Find ways to delete value in reference item. The proper way is to expose each of those child entity as API
# We have set parameter in client into json instead of multipart form, maybe we should explicitly set it.
class PersonAPITestCase(APITestCase):

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

    def test_view_person_list(self):
        response = self.client.get("/en/persons/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_person_detail(self):
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        response = self.client.get("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["result"]["name"], "John")

    def test_view_person_detail_not_exist(self):
        response = self.client.get("/en/persons/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_person_unauthorized(self):
        person_data = {
            "name": "joe",
            "family_name": "doe",
            "given_name": "joe jambul",
            "additional_name": "not john doe",
            "gender": "unknown",
            "summary": "person unit test api",
            "honorific_prefix": "Chief",
            "honorific_suffix": "of the fake people league",
            "biography": "He does not exists!!!!",
            "birth_date": "1950-01-01",
            "death_data": "2000-01-01",
            "email": "joejambul@sinarproject.org",
            "contact_details":[
                {
                    "type":"twitter",
                    "value": "sinarproject",
                }
            ],
            "links":[
                {
                    "url":"http://sinarproject.org",
                }
            ],
            "identifiers":[
                {
                    "identifier": "9089098098",
                    "scheme": "rakyat",
                }
            ],
            "other_names":[
                {
                    "name":"Jane",
                    "family_name":"Jambul",
                    "start_date": "1950-01-01",
                    "end_date": "2010-01-01",
                }
            ]
        }

        response = self.client.post("/en/persons/", person_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_person_authorized(self):
        person_data = {
            "name": "joe",
            "family_name": "doe",
            "given_name": "joe jambul",
            "additional_name": "not john doe",
            "gender": "unknown",
            "summary": "person unit test api",
            "honorific_prefix": "Chief",
            "honorific_suffix": "of the fake people league",
            "biography": "He does not exists!!!!",
            "birth_date": "1950-01-01",
            "death_data": "2000-01-01",
            "email": "joejambul@sinarproject.org",
            "contact_details":[
                {
                    "type":"twitter",
                    "value": "sinarproject",
                }
            ],
            "links":[
                {
                    "url":"http://sinarproject.org",
                }
            ],
            "identifiers":[
                {
                    "identifier": "9089098098",
                    "scheme": "rakyat",
                }
            ],
            "other_names":[
                {
                    "name":"Jane",
                    "family_name":"Jambul",
                    "start_date": "1950-01-01",
                    "end_date": "2010-01-01",
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/persons/", person_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        person = Person.objects.language("en").get(name="joe")
        self.assertEqual(person.name, "joe")
        self.client.credentials()

    def test_update_person_unauthorized(self):
        person_data = {
            "given_name": "jerry jambul",
        }
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/", person_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_not_exist_unauthorized(self):
        person_data = {
            "given_name": "jerry jambul",
        }
        response = self.client.put("/en/persons/not_exist/", person_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_authorized(self):
        person_data = {
            "given_name": "jerry jambul",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/", person_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        self.assertEqual(person_.given_name, "jerry jambul")

    def test_update_person_not_exist_authorized(self):
        person_data = {
            "given_name": "jerry jambul",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/persons/not_exist/", person_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_person_links_unauthorized(self):
        person_data = {
            "links": [
                {
                    "url": "http://twitter.com/sweemeng",
                }
            ]
        }
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/", person_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_person_links_authorized(self):
        person_data = {
            "links": [
                {
                    "url": "http://twitter.com/sweemeng",
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/", person_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        url = person_.links.language("en").get(url="http://twitter.com/sweemeng")
        self.assertEqual(url.url, "http://twitter.com/sweemeng")

    def test_update_person_links_unauthorized(self):
        person_data = {
            "id":"ab1a5788e5bae955c048748fa6af0e97",
            "links":[
                {
                    "id": "a4ffa24a9ef3cbcb8cfaa178c9329367",
                    "note": "just a random repo"
                }
            ]
        }
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/", person_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_links_authorized(self):
        person_data = {
            "id":"ab1a5788e5bae955c048748fa6af0e97",
            "links":[
                {
                    "id": "a4ffa24a9ef3cbcb8cfaa178c9329367",
                    "note": "just a random repo"
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/", person_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        url = person_.links.language("en").get(id="a4ffa24a9ef3cbcb8cfaa178c9329367")
        self.assertEqual(url.note, "just a random repo")

    def test_create_nested_person_links_unauthorized(self):
        person_data = {
            "id":"ab1a5788e5bae955c048748fa6af0e97",
            "contact_details":[
                {
                    "id": "a66cb422-eec3-4861-bae1-a64ae5dbde61",
                    "links": [{
                        "url": "http://facebook.com",
                    }]
                }
            ],
        }
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/", person_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_nested_person_links_authorized(self):
        person_data = {
            "id":"ab1a5788e5bae955c048748fa6af0e97",
            "contact_details":[
                {
                    "id": "a66cb422-eec3-4861-bae1-a64ae5dbde61",
                    "links": [{
                        "url": "http://facebook.com",
                    }]
                }
            ],
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/", person_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        # There should be only 1 links in that contact
        contact = person_.contact_details.language('en').get(id='a66cb422-eec3-4861-bae1-a64ae5dbde61')
        links = contact.links.language('en').all()
        self.assertEqual(links[0].url, "http://facebook.com")

    def test_update_nested_person_links_unauthorized(self):
        person_data = {
            "id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "identifiers":[
                {
                    "id": "af7c01b5-1c4f-4c08-9174-3de5ff270bdb",
                    "links": [{
                        "id": "9c9a2093-c3eb-4b51-b869-0d3b4ab281fd",
                        "note": "this is just a test note",
                    }]
                }
            ],
        }
        response = self.client.put("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/", person_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_nested_person_links_authorized(self):
        person_data = {
            "id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "identifiers":[
                {
                    "id": "af7c01b5-1c4f-4c08-9174-3de5ff270bdb",
                    "links": [{
                        "id": "9c9a2093-c3eb-4b51-b869-0d3b4ab281fd",
                        "note": "this is just a test note",
                    }]
                }
            ],
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/", person_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person_ = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        identifier = person_.identifiers.language('en').get(id="af7c01b5-1c4f-4c08-9174-3de5ff270bdb")
        link = identifier.links.language('en').get(id="9c9a2093-c3eb-4b51-b869-0d3b4ab281fd")
        self.assertEqual(link.note, "this is just a test note")

    def test_create_identifier_unauthorized(self):
        person_data = {
            "identifiers": [
                {
                    "scheme": "IC",
                    "identifier": "129031309",
                }
            ]
        }
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/", person_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_identifier_authorized(self):
        person_data = {
            "identifiers": [
                {
                    "scheme": "IC",
                    "identifier": "129031309",
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/", person_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')

        identifier = person_.identifiers.language('en').get(identifier="129031309")
        self.assertEqual(identifier.scheme, "IC")

    def test_update_identifier_unauthorized(self):
        person_data = {
            "identifiers": [
                {
                    "id": "34b59cb9-607a-43c7-9d13-dfe258790ebf",
                    "identifier": "53110322",
                }
            ]
        }
        # 8497ba86-7485-42d2-9596-2ab14520f1f4
        response = self.client.put("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/", person_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_identifier_authorized(self):
        person_data = {
            "identifiers": [
                {
                    "id": "34b59cb9-607a-43c7-9d13-dfe258790ebf",
                    "identifier": "53110322",
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/", person_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person_ = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        identifier = person_.identifiers.language('en').get(id="34b59cb9-607a-43c7-9d13-dfe258790ebf")
        self.assertEqual(identifier.identifier, '53110322')

    def test_create_contact_unauthorized(self):
        person_data = {
            "contact_details": [
                {
                    "type":"twitter",
                    "value": "sinarproject",
                }
            ]
        }
        # 8497ba86-7485-42d2-9596-2ab14520f1f4
        response = self.client.put("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/", person_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_contact_authorized(self):
        person_data = {
            "contact_details": [
                {
                    "type":"twitter",
                    "value": "sinarproject",
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/", person_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        person_ = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        contact = person_.contact_details.language('en').get(type="twitter")
        self.assertEqual(contact.value, "sinarproject")

    def test_update_contact_unauthorized(self):
        person_data = {
            "contact_details": [
                {
                    "id": "a66cb422-eec3-4861-bae1-a64ae5dbde61",
                    "value": "0123421222",
                }
            ]
        }
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/", person_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_contact_authorized(self):
        person_data = {
            "contact_details": [
                {
                    "id": "a66cb422-eec3-4861-bae1-a64ae5dbde61",
                    "value": "0123421222",
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/", person_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        contact = person_.contact_details.language('en').get(id="a66cb422-eec3-4861-bae1-a64ae5dbde61")
        self.assertEqual(contact.value, "0123421222")

    def test_create_other_names_unauthorized(self):
        person_data = {
            "other_names": [
                {
                    "name": "jane",
                    "family_name": "jambul",
                    "given_name": "test person",
                    "start_date": "1950-01-01",
                    "end_date": "2010-01-01",
                }
            ]
        }
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/", person_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_other_names_authorized(self):
        person_data = {
            "other_names": [
                {
                    "name": "jane",
                    "family_name": "jambul",
                    "given_name": "test person",
                    "start_date": "1950-01-01",
                    "end_date": "2010-01-01",
                }
            ]
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/", person_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        other_name = person_.other_names.language('en').get(name="jane")
        self.assertEqual(other_name.given_name, "test person")

    def test_update_other_names_unauthorized(self):
        person_data = {
            "other_names": [
                {
                    "id": "cf93e73f-91b6-4fad-bf76-0782c80297a8",
                    "family_name": "jambul",
                }
            ]
        }
        response = self.client.put("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/", person_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_other_names_authorized(self):
        person_data = {
            "other_names": [
                {
                    "id": "cf93e73f-91b6-4fad-bf76-0782c80297a8",
                    "family_name": "jambul",
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/", person_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person_ = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        other_name = person_.other_names.language('en').get(id="cf93e73f-91b6-4fad-bf76-0782c80297a8")
        self.assertEqual(other_name.family_name, "jambul")

    def test_delete_persons_unauthorized(self):
        response = self.client.delete("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_not_exist_unauthorized(self):
        response = self.client.delete("/en/persons/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_persons_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_person_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/persons/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
