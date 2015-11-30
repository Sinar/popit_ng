from django.test import TestCase
from django.test import override_settings
from popit_search.utils import search
from popit.models import Person
from popit.serializers import PersonSerializer
import requests
from rest_framework import status
from django.conf import settings
import logging
import time
# Create your tests here.


@override_settings(ES_INDEX="test_popit")
class SearchUtilTestCase(TestCase):
    fixtures = [ "api_request_test_data.yaml" ]

    def setUp(self):
        self.popit_search = search.SerializerSearch("persons", index="test_popit")
        self.es_host = settings.ES_HOST[0]

    def tearDown(self):
        self.popit_search.delete_index()

    def test_index_person(self):
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")

        result = self.popit_search.add(person, PersonSerializer)
        self.assertTrue(result["created"])
        check = requests.get("%s/%s/person/%s" % (self.es_host, "test_popit", result["_id"]))
        self.assertEqual(check.status_code, status.HTTP_200_OK)

    def test_search_person(self):
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        result = self.popit_search.add(person, PersonSerializer)
        search_result = self.popit_search.search("id:ab1a5788e5bae955c048748fa6af0e97", language="en")
        self.assertNotEqual(search_result, [])

    def test_search_person_not_exist(self):
        search_result = self.popit_search.search("id:not_exist", language="en")
        self.assertEqual(search_result, [])

    def test_update_person_search(self):
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        result = self.popit_search.add(person, PersonSerializer)

        self.assertTrue(result["created"])
        person.given_name = "jerry jambul"
        person.save()
        result = self.popit_search.update(person, PersonSerializer)
        check = requests.get("%s/%s/person/%s" % (self.es_host, "test_popit", result["_id"]))
        output = check.json()
        self.assertEqual(check.status_code, status.HTTP_200_OK)
        self.assertEqual(output["_source"]["given_name"], "jerry jambul")

    def test_delete_person_search(self):
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        result = self.popit_search.add(person, PersonSerializer)

        self.popit_search.delete(person)
        search_result = self.popit_search.search("id:ab1a5788e5bae955c048748fa6af0e97", language="en")
        self.assertEqual(search_result, [])