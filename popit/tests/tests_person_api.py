__author__ = 'sweemeng'
from rest_framework import status
from popit.signals.handlers import *
from popit.models import *
from django.conf import settings
import json
import logging
from popit.tests.base_testcase import BasePopitTestCase
from popit.tests.base_testcase import BasePopitAPITestCase


# TODO: Test multilingual behavior. To make behavior clear
# TODO: Need new fixtures
class PersonSerializerTestCase(BasePopitTestCase):

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
        person = Person.objects.untranslated().get(id='078541c9-9081-4082-b28f-29cbb64440cb')
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
        person_serializer = PersonSerializer(person, data=person_data, partial=True, language="en")
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
        links = contact.links.language('en').filter(url="http://sinarproject.org")
        self.assertEqual(links[0].url, "http://sinarproject.org")

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
        person_serializer = PersonSerializer(person, data=person_data, partial=True, language="en")
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

    def test_create_person_invalid_date_serializer(self):
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
            "birth_date": "invalid date",
            "death_data": "invalid date",
            "email": "joejambul@sinarproject.org",
        }
        person_serial = PersonSerializer(data=person_data, language='en')
        person_serial.is_valid()
        self.assertNotEqual(person_serial.errors, {})

    def test_update_person_translated_serializer(self):
        person_data = {
            "given_name": "jerry jambul",
        }

        person = Person.objects.language("ms").get(id='ab1a5788e5bae955c048748fa6af0e97')

        person_serializer = PersonSerializer(person, data=person_data, partial=True, language='ms')
        person_serializer.is_valid()
        self.assertEqual(person_serializer.errors, {})
        person_serializer.save()
        person_ = Person.objects.language('ms').get(id='ab1a5788e5bae955c048748fa6af0e97')
        self.assertEqual(person_.given_name, "jerry jambul")

    def test_create_person_translated_serializer(self):
        person_data = {
            "name": "joe",
            "family_name": "doe",
            "given_name": "joe jambul",
            "additional_name": "bukan john doe",
            "gender": "tak tahu",
            "summary": "orang ujian",
            "honorific_prefix": "Datuk Seri",
            "biography": "Dia Tak wujud!!!!",
            "email": "joejambul@sinarproject.org",
        }

        person_serial = PersonSerializer(data=person_data, language='ms')
        person_serial.is_valid()
        self.assertEqual(person_serial.errors, {})
        person_serial.save()
        person = Person.objects.language("ms").get(name="joe")
        self.assertEqual(person.given_name, "joe jambul")

    def test_load_translated_person_membership(self):
        person = Person.objects.untranslated().get(id="078541c9-9081-4082-b28f-29cbb64440cb")
        person_serializer = PersonSerializer(person, language="ms")
        data = person_serializer.data
        for membership in data["memberships"]:
            self.assertEqual(membership["language_code"], "ms")

    def test_load_translated_person_membership_organization(self):
        person = Person.objects.untranslated().get(id="078541c9-9081-4082-b28f-29cbb64440cb")
        person_serializer = PersonSerializer(person, language="ms")
        data = person_serializer.data
        for membership in data["memberships"]:
            if membership["organization"]:
                self.assertEqual(membership["organization"]["language_code"], "ms")

    def test_fetch_person_membership_on_behalf_of_expanded(self):
        person = Person.objects.untranslated().get(id="2439e472-10dc-4f9c-aa99-efddd9046b4a")
        person_serializer = PersonSerializer(person, language="en")
        data = person_serializer.data
        self.assertEqual(data["memberships"][0]["on_behalf_of"]["id"], "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
            

# We have set parameter in client into json instead of multipart form, maybe we should explicitly set it.
class PersonAPITestCase(BasePopitAPITestCase):

    def test_view_person_list(self):
        response = self.client.get("/en/persons/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("page" in response.data)
        self.assertEqual(response.data["per_page"], settings.REST_FRAMEWORK["PAGE_SIZE"])
        self.assertEqual(response.data["num_pages"], 1)

    def test_view_person_detail(self):
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        response = self.client.get("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["result"]["name"], "John")
        self.assertTrue("memberships" in response.data["result"])

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
        check = False
        for i in links:
            if i.url == "http://sinarproject.org":
                check = True
        self.assertTrue(check, "http://sinarproject.org does not exist")

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

    def test_person_api_summary_more_than_255(self):
        raw_data = """
            {

                "result":

                    {

                        "proxy_image": "https://sinar-malaysia.popit.mysociety.org/image-proxy/http%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F0%2F05%2FAnwar_Ibrahim.jpg%2F398px-Anwar_Ibrahim.jpg",
                        "image": "http://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Anwar_Ibrahim.jpg/398px-Anwar_Ibrahim.jpg",
                        "html_url": "https://sinar-malaysia.popit.mysociety.org/persons/53630562f1eab6270da6c8ed",
                        "url": "https://sinar-malaysia.popit.mysociety.org/api/v0.1/persons/53630562f1eab6270da6c8ed",
                        "birth_date": "1947-08-10",
                        "death_date": null,
                        "id": "53630562f1eab6270da6c8ed",
                        "name": "Anwar Ibrahim",
                        "summary": "Dato' Seri Anwar Bin Ibrahim[1] (born 10 August 1947) is a Malaysian politician. He is the Leader of Opposition of Malaysia (Pakatan Rakyat), economic advisor to the state government of Selangor[2] and de facto leader of PKR (KeADILan). He served as the Deputy Prime Minister of Malaysia from 1993 to 1998 and Finance Minister from 1991 to 1998 when he was in UMNO, a major party in ruling Barisan Nasional coaltion.",
                        "images":

                        [

                            {
                                "proxy_url": "https://sinar-malaysia.popit.mysociety.org/image-proxy/http%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F0%2F05%2FAnwar_Ibrahim.jpg%2F398px-Anwar_Ibrahim.jpg",
                                "created": "",
                                "url": "http://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Anwar_Ibrahim.jpg/398px-Anwar_Ibrahim.jpg",
                                "id": "536305bef1eab6270da6c8ee"
                            }

                        ],
                        "memberships":
                        [

                            {

                                "contact_details": [ ],
                                "links": [ ],
                                "images": [ ],
                                "url": "https://sinar-malaysia.popit.mysociety.org/api/v0.1/memberships/53630b0619ee29270d8a9e5e",
                                "start_date": null,
                                "role": "",
                                "post_id": null,
                                "person_id": "53630562f1eab6270da6c8ed",
                                "organization_id": "536309c319ee29270d8a9e26",
                                "label": null,
                                "id": "53630b0619ee29270d8a9e5e",
                                "html_url": "https://sinar-malaysia.popit.mysociety.org/memberships/53630b0619ee29270d8a9e5e",
                                "end_date": null,
                                "area_name": null,
                                "area_id": null

                            },
                            {

                                "contact_details": [ ],
                                "links": [ ],
                                "images": [ ],
                                "id": "53633d8319ee29270d8a9ed5",
                                "person_id": "53630562f1eab6270da6c8ed",
                                "end_date": "2013-05-05",
                                "start_date": "2008-08-26",
                                "label": null,
                                "post_id": "53633d1719ee29270d8a9ed4",
                                "role": "Opposition Leader",
                                "organization_id": "53633b5a19ee29270d8a9ecf",
                                "url": "https://sinar-malaysia.popit.mysociety.org/api/v0.1/memberships/53633d8319ee29270d8a9ed5",
                                "html_url": "https://sinar-malaysia.popit.mysociety.org/memberships/53633d8319ee29270d8a9ed5"

                            },
                            {

                                "contact_details": [ ],
                                "links": [ ],
                                "images": [ ],
                                "end_date": null,

                                "id": "5535e892aea781383fa79402",
                                "post_id": "545e4d5b5222837c2c05988b",
                                "start_date": "2013",
                                "role": "Parliamentary Candidate",
                                "organization_id": "545de8665222837c2c0586c0",
                                "person_id": "53630562f1eab6270da6c8ed",
                                "url": "https://sinar-malaysia.popit.mysociety.org/api/v0.1/memberships/5535e892aea781383fa79402",
                                "html_url": "https://sinar-malaysia.popit.mysociety.org/memberships/5535e892aea781383fa79402"
                            }

                        ],
                        "links": [ ],
                        "contact_details": [ ],
                        "identifiers": [ ],
                        "other_names":
                        [

                        {

                            "name": "Dato' Seri Anwar Bin Ibrahim",
                            "note": "With honorifics.",
                            "id": "55653036561fa5421bb7bd20"

                        },

                                    {
                                        "name": "Anwar Bin Ibrahim",
                                        "id": "55653036561fa5421bb7bd1f"
                                    }
                                ]
                            }

                        }
            """
        data = json.loads(raw_data)
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/persons/", data["result"])
        logging.warn(response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_person_api_invalid_date(self):
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
            "birth_date": "invalid date",
            "death_date": "invalid date",
            "email": "joejambul@sinarproject.org",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/persons/", person_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("errors" in response.data)

    def test_update_person_authorized_translated(self):
        person_data = {
            "given_name": "jerry jambul",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/ms/persons/ab1a5788e5bae955c048748fa6af0e97/", person_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person_ = Person.objects.language('ms').get(id='ab1a5788e5bae955c048748fa6af0e97')
        self.assertEqual(person_.given_name, "jerry jambul")

    def test_create_person_authorized_translated(self):
        person_data = {
            "name": "joe",
            "family_name": "doe",
            "given_name": "joe jambul",
            "additional_name": "bukan john doe",
            "gender": "tak tahu",
            "summary": "orang ujian",
            "honorific_prefix": "Datuk Seri",
            "biography": "Dia Tak wujud!!!!",
            "email": "joejambul@sinarproject.org",
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/ms/persons/", person_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        person = Person.objects.language("ms").get(name="joe")
        self.assertEqual(person.name, "joe")

    def test_create_person_othername_blank_id_authorized(self):
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

            "other_names":[
                {
                    "id": "",
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
        logging.warn(response.data["result"]["other_names"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        other_names = response.data["result"]["other_names"][0]
        self.assertNotEqual(other_names["id"], "")

    def test_create_person_identifier_blank_id_authorized(self):
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

            "identifiers":[
                {
                    "id": "",
                    "identifier": "9089098098",
                    "scheme": "rakyat",
                }
            ],
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/persons/", person_data)
        logging.warn(response.data["result"]["other_names"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        identifiers = response.data["result"]["identifiers"][0]
        self.assertNotEqual(identifiers["id"], "")

    def test_create_person_contact_details_blank_id_authorized(self):
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
                    "id": "",
                    "type":"twitter",
                    "value": "sinarproject",
                }
            ],
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/persons/", person_data)
        logging.warn(response.data["result"]["other_names"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        contact_details = response.data["result"]["contact_details"][0]
        self.assertNotEqual(contact_details["id"], "")

    def test_create_person_links_blank_id_authorized(self):
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
            "links":[
                {
                    "id": "",
                    "url":"http://sinarproject.org",
                }
            ],
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/persons/", person_data)
        logging.warn(response.data["result"]["other_names"])
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        links = response.data["result"]["links"][0]
        self.assertNotEqual(links["id"], "")

    def test_create_person_with_all_field_blank_id_serializer(self):

        person_data = {
            "id": "",
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

    def test_create_person_with_all_field_birthdate_deathdate_blank_serializer(self):
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
            "birth_date": "",
            "death_data": "",
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

    def test_minify_person_api(self):
        
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97", {"minify":"True"})

        self.assertTrue("memberships" not in response.data["result"])
