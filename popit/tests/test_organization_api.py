__author__ = 'sweemeng'
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from popit.models import Organization
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from popit.signals.handlers import *
from popit.models import *
import logging
import requests
from django.conf import settings
import json
import os

class OrganizationAPITestCase(APITestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    def setUp(self):
        post_save.disconnect(entity_save_handler, sender=Person)
        post_save.disconnect(entity_save_handler, sender=Organization)
        post_save.disconnect(entity_save_handler, sender=Membership)
        post_save.disconnect(entity_save_handler, sender=Post)
        post_save.disconnect(entity_save_handler, sender=Membership)
        post_save.disconnect(entity_save_handler, sender=ContactDetail)
        post_save.disconnect(entity_save_handler, sender=Identifier)
        post_save.disconnect(entity_save_handler, sender=OtherName)
        post_save.disconnect(entity_save_handler, sender=Link)

        pre_delete.disconnect(entity_prepare_delete_handler, sender=Person)
        pre_delete.disconnect(entity_prepare_delete_handler, sender=Organization)
        pre_delete.disconnect(entity_prepare_delete_handler, sender=Membership)
        pre_delete.disconnect(entity_prepare_delete_handler, sender=Post)
        pre_delete.disconnect(entity_prepare_delete_handler, sender=ContactDetail)
        pre_delete.disconnect(entity_prepare_delete_handler, sender=Identifier)
        pre_delete.disconnect(entity_prepare_delete_handler, sender=OtherName)
        pre_delete.disconnect(entity_prepare_delete_handler, sender=Link)

        post_delete.disconnect(entity_perform_delete_handler, sender=Person)
        post_delete.disconnect(entity_perform_delete_handler, sender=Organization)
        post_delete.disconnect(entity_perform_delete_handler, sender=Membership)
        post_delete.disconnect(entity_perform_delete_handler, sender=Post)
        post_delete.disconnect(entity_perform_delete_handler, sender=ContactDetail)
        post_delete.disconnect(entity_perform_delete_handler, sender=Identifier)
        post_delete.disconnect(entity_perform_delete_handler, sender=OtherName)
        post_delete.disconnect(entity_perform_delete_handler, sender=Link)

    def tearDown(self):
        post_save.connect(entity_save_handler, sender=Person)
        post_save.connect(entity_save_handler, sender=Organization)
        post_save.connect(entity_save_handler, sender=Membership)
        post_save.connect(entity_save_handler, sender=Post)
        post_save.connect(entity_save_handler, sender=Membership)
        post_save.connect(entity_save_handler, sender=ContactDetail)
        post_save.connect(entity_save_handler, sender=Identifier)
        post_save.connect(entity_save_handler, sender=OtherName)
        post_save.connect(entity_save_handler, sender=Link)

        pre_delete.connect(entity_prepare_delete_handler, sender=Person)
        pre_delete.connect(entity_prepare_delete_handler, sender=Organization)
        pre_delete.connect(entity_prepare_delete_handler, sender=Membership)
        pre_delete.connect(entity_prepare_delete_handler, sender=Post)
        pre_delete.connect(entity_prepare_delete_handler, sender=ContactDetail)
        pre_delete.connect(entity_prepare_delete_handler, sender=Identifier)
        pre_delete.connect(entity_prepare_delete_handler, sender=OtherName)
        pre_delete.connect(entity_prepare_delete_handler, sender=Link)

        post_delete.connect(entity_perform_delete_handler, sender=Person)
        post_delete.connect(entity_perform_delete_handler, sender=Organization)
        post_delete.connect(entity_perform_delete_handler, sender=Membership)
        post_delete.connect(entity_perform_delete_handler, sender=Post)
        post_delete.connect(entity_perform_delete_handler, sender=ContactDetail)
        post_delete.connect(entity_perform_delete_handler, sender=Identifier)
        post_delete.connect(entity_perform_delete_handler, sender=OtherName)
        post_delete.connect(entity_perform_delete_handler, sender=Link)


    def test_view_organization_list(self):
        response = self.client.get("/en/organizations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("page" in response.data)
        self.assertEqual(response.data["per_page"], settings.REST_FRAMEWORK["PAGE_SIZE"])

    def test_view_organization_list_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get("/en/organizations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_organization_detail(self):
        response = self.client.get("/en/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("memberships" in response.data["result"])
        self.assertTrue("posts" in response.data["result"])

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
            "contact_details": [
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
            "contact_details": [
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
        contact = organization.contact_details.language("en").get(label="myphone")
        self.assertEqual(contact.value, "01234567")

    def test_update_organization_contact_unauthorized(self):
        data = {
            "contact_details": [
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
            "contact_details": [
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
        contact = organization.contact_details.language("en").get(id="651da7cd-f109-4aaa-b04c-df835fb6831f")
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
            "contact_details": [
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
            "contact_details": [
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
        contact = organization.contact_details.language("en").get(id="651da7cd-f109-4aaa-b04c-df835fb6831f")
        link = contact.links.language("en").get(url="http://google.com")
        self.assertEqual(link.url, "http://google.com")

    def test_update_nested_link_organization_contact_unauthorized(self):
        data = {
            "contact_details": [
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
            "contact_details": [
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
        contact = organization.contact_details.language("en").get(id="651da7cd-f109-4aaa-b04c-df835fb6831f")
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

    def test_fetch_organization_translated(self):
        response = self.client.get("/ms/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/")
        results = response.data["result"]
        self.assertEqual(results["name"], "Parti Lanun KL")
        self.assertEqual(results["language_code"], "ms")

    def test_fetch_organization_translated_nested(self):
        response = self.client.get("/ms/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/")
        results = response.data["result"]
        self.assertEqual(results["parent"]["language_code"], "ms")

    def test_import_error_organization(self):
        path = os.path.abspath(os.path.curdir)
        data = json.load(open(os.path.join(path,"popit/fixtures/mysociety_popit_org_1.json")))
        target = None
        for item in data["result"]:
            if item["id"] == "5362fcc219ee29270d8a9e22":
                target = item
        if target:
            token = Token.objects.get(user__username="admin")
            self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
            response = self.client.post("/en/organizations/", target)
            logging.warn(response.data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_organization_invalid_date(self):
        data = {
            "name": "acme corp",
            "founding_date": "invalid date",
            "dissolution_date": "invalid date"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/organizations/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("errors" in response.data)

    def test_create_organization_valid_date(self):
        data = {
            "name": "acme corp",
            "founding_date": "2010-01-01",
            "dissolution_date": "2015-01-01",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/organizations/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_organization_invalid_parent(self):
        data = {
            "name": "acme corp",
            "parent_id": "not exist"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/organizations/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("errors" in response.data)

    def test_create_organization_valid_parent(self):
        data = {
            "name": "acme corp",
            "parent_id": "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/organizations/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_organization_invalid_area_id(self):
        data = {
            "name": "acme corp",
            "area_id": "not exist"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/organizations/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("errors" in response.data)

    def test_create_organization_translated(self):
        data = {
            "name": "acme sdn bhd",
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/ms/organizations/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_organization_authorized_translated(self):
        data = {
            "abstract": "Cawangan KL Parti Lanun Malaysia"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/ms/organizations/3d62d9ea-0600-4f29-8ce6-f7720fd49aa3/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        organization = Organization.objects.language("ms").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        self.assertEqual(organization.abstract, "Cawangan KL Parti Lanun Malaysia")

    def test_create_organization_real_data(self):
        raw_data = """
            {

                "result": {
                    "proxy_image": "https://sinar-malaysia.popit.mysociety.org/image-proxy/http%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F1%2F1e%2FParti_Keadilan_Rakyat_logo.svg%2F800px-Parti_Keadilan_Rakyat_logo.svg.png",
                    "image": "http://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Parti_Keadilan_Rakyat_logo.svg/800px-Parti_Keadilan_Rakyat_logo.svg.png",
                    "birth_date": null,
                    "death_date": null,
                    "html_url": "https://sinar-malaysia.popit.mysociety.org/organizations/536309c319ee29270d8a9e26",
                    "id": "536309c319ee29270d8a9e26",
                    "name": "People's Justice Party",
                    "summary": "The People's Justice Party (Malay: Parti Keadilan Rakyat , often known simply as KeADILan or PKR) is a centrist multiracial political party in Malaysia formed in 2003 by a merger of the National Justice Party and the older Malaysian People's Party. Keadilan was led by Dr Wan Azizah Wan Ismail and increased its parliamentary representation from 1 seat to 31 seats in the Malaysian general election, 2008 until the five-year political ban imposed on former Deputy Prime Minister Anwar Ibrahim was lifted on 14 April 2008. This party enjoys strong support from the urban state such as Selangor and Penang.",
                    "url": "https://sinar-malaysia.popit.mysociety.org/api/v0.1/organizations/536309c319ee29270d8a9e26",
                    "classification": "Party",
                    "dissolution_date": "",
                    "founding_date": "",
                    "parent_id": "",
                    "images": [
                        {
                            "proxy_url": "https://sinar-malaysia.popit.mysociety.org/image-proxy/http%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2F1%2F1e%2FParti_Keadilan_Rakyat_logo.svg%2F800px-Parti_Keadilan_Rakyat_logo.svg.png",
                            "created": "",
                            "url": "http://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Parti_Keadilan_Rakyat_logo.svg/800px-Parti_Keadilan_Rakyat_logo.svg.png",
                            "id": "536309edf1eab6270da6c8ef"
                        }
                    ],
                    "posts": [ ],
                    "memberships": [

                        {

                            "contact_details": [ ],
                            "links": [ ],
                            "images": [ ],
                            "area":

                            {
                                "name": ""
                            },
                            "url": "https://sinar-malaysia.popit.mysociety.org/api/v0.1/memberships/53630b0619ee29270d8a9e5e",
                            "start_date": "",
                            "role": "",
                            "post_id": null,
                            "person_id": "53630562f1eab6270da6c8ed",
                            "organization_id": "536309c319ee29270d8a9e26",
                            "label": null,
                            "id": "53630b0619ee29270d8a9e5e",
                            "html_url": "https://sinar-malaysia.popit.mysociety.org/memberships/53630b0619ee29270d8a9e5e",
                            "end_date": "",
                            "area_name": null,
                            "area_id": null

                        },
                        {

                            "contact_details": [ ],
                            "links": [ ],
                            "images": [ ],
                            "area":

                            {
                                "name": ""
                            },
                            "id": "5363529319ee29270d8a9eea",
                            "person_id": "53635149f1eab6270da6c8f6",
                            "area_name": null,
                            "area_id": null,
                            "end_date": "",
                            "start_date": "",
                            "label": null,
                            "post_id": "5363526819ee29270d8a9ee9",
                            "role": "",
                            "organization_id": "536309c319ee29270d8a9e26",
                            "url": "https://sinar-malaysia.popit.mysociety.org/api/v0.1/memberships/5363529319ee29270d8a9eea",
                            "html_url": "https://sinar-malaysia.popit.mysociety.org/memberships/5363529319ee29270d8a9eea"

                        },
                        {

                            "contact_details": [ ],
                            "links": [ ],
                            "images": [ ],
                            "id": "555968759e14806704785cb9",
                            "area":

                                {
                                    "name": ""
                                },
                                "end_date": "",
                                "start_date": "",
                                "organization_id": "536309c319ee29270d8a9e26",
                                "role": "Member",
                                "person_id": "53635149f1eab6270da6c8f6",
                                "url": "https://sinar-malaysia.popit.mysociety.org/api/v0.1/memberships/555968759e14806704785cb9",
                                "html_url": "https://sinar-malaysia.popit.mysociety.org/memberships/555968759e14806704785cb9"
                            }

                    ],
                    "links": [

                        {
                            "url": "http://www.keadilanrakyat.org/",
                            "note": "Main website",
                            "id": "545e11b05222837c2c058722"
                        }

                    ],
                    "contact_details": [

                        {

                            "label": "Email",
                            "type": "Email",
                            "value": "ibupejabat@keadilanrakyat.org",
                            "note": "",
                            "id": "545e11b05222837c2c058721"

                        },
                        {

                            "label": "Fax",
                            "type": "Fax",
                            "value": "+603 - 7885 0531",
                            "note": "",
                            "id": "545e11b05222837c2c058720"

                        },

                        {
                            "label": "Phone",
                            "type": "Phone",
                            "value": "+603 - 7885 0530",
                            "note": "",
                            "id": "545e11b05222837c2c05871f"
                        }

                    ],
                    "identifiers": [ ],
                    "other_names": [

                        {

                            "name": "KeADILan",
                            "start_date": "",
                            "end_date": "",
                            "note": "",
                            "id": "545e11b05222837c2c058728"

                        },
                        {

                            "name": "PKR",
                            "start_date": "",
                            "end_date": "",
                            "note": "Abbreviation",
                            "id": "545e11b05222837c2c058727"

                        },

                        {
                            "name": "Parti Keadilan Rakyat",
                            "start_date": "",
                            "end_date": "",
                            "note": "Bahasa",
                            "id": "545e11b05222837c2c058723"
                        }
                    ]
                }

            }

        """
        data = json.loads(raw_data)
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/organizations/", data["result"])
        logging.warn(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_organization_blank_id_authorized(self):
        data = {
            "id": "",
            "name": "acme corp"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/organizations/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        organization = Organization.objects.language("en").get(name="acme corp")
        self.assertEqual(organization.name, "acme corp")