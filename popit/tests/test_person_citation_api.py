from rest_framework.test import APITestCase
from popit.signals.handlers import *
from popit.models import *
from rest_framework import status
import logging


class PersonCitationAPITestCase(APITestCase):
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

    def test_fetch_person_field_citation(self):
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/citations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        person = Person.objects.language("en").get(id="ab1a5788e5bae955c048748fa6af0e97")
        for field in person._meta.fields:
            if field.attname == "id":
                continue
            self.assertTrue(field.attname in data["result"])
        for field in person._translated_field_names:
            if field == "master_id" or field == "id":
                continue
            self.assertTrue(field in data["result"])

    def test_fetch_person_citation_list(self):
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/citations/email/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(len(data["results"]), 1)

    def test_fetch_person_citation_not_exists(self):
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/citations/email/not_exists/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fetch_person_citation_exists(self):
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/citations/email/7e462cdea35840a28c20cf9fe79284fd/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["result"]["url"], "http://sinarproject.org")

    def test_add_person_citation_unauthorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }

        response = self.client.post("/en/persons/ab1a5788e5bae955c048748fa6af0e97/citations/name/", data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_person_citation_authorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/persons/ab1a5788e5bae955c048748fa6af0e97/citations/name/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_person_citation_unauthorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/citations/email/7e462cdea35840a28c20cf9fe79284fd/"
                                   , data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_api_authorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/citations/email/7e462cdea35840a28c20cf9fe79284fd/"
            , data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
