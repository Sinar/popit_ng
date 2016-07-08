__author__ = 'sweemeng'
from django.test import TestCase
from popit.serializers import OrganizationSerializer
from popit.models import Organization
from popit.signals.handlers import *
from popit.models import *


class OrganizationSerializerTestCase(TestCase):
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


    def test_fetch_organization_serializer(self):
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, language="en")
        data = serializer.data

        self.assertEqual(data["name"], "Pirate Party KL")

    def test_create_organization_serializer(self):
        data = {
            "name": "acme corp"
        }
        serializer = OrganizationSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        organization = Organization.objects.language("en").get(name="acme corp")
        self.assertEqual(organization.name, "acme corp")

    def test_update_organization_serializer(self):
        data = {
            "abstract": "KL Branch of Pirate Party Malaysia"
        }
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        self.assertEqual(organization.abstract, "KL Branch of Pirate Party Malaysia")

    def test_create_organization_othername_serializer(self):
        data = {
            "other_names":[
                {
                    "name": "Not FSociety"
                }
            ]
        }

        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        other_name = organization.other_names.language("en").get(name="Not FSociety")
        self.assertEqual(other_name.name, "Not FSociety")

    def test_update_organization_othername_serializer(self):
        data = {
            "other_names": [
                {
                    "id" : "53a22b00-1383-4bf5-b4be-4753d8d16062",
                    "note" : "Other Name of Pirate Party"
                }
            ]
        }
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        other_name = organization.other_names.language("en").get(id="53a22b00-1383-4bf5-b4be-4753d8d16062")
        self.assertEqual(other_name.note, "Other Name of Pirate Party")

    def test_create_organization_identifier_serializer(self):
        data = {
            "identifiers": [
                {
                    "scheme": "testing",
                    "identifier": "12319021390"
                }
            ]
        }
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        identifier = organization.identifiers.language("en").get(identifier="12319021390")
        self.assertEqual(identifier.scheme, "testing")

    def test_update_organization_identifier_serializer(self):
        data = {
            "identifiers": [
                {
                    "id": "2d3b8d2c-77b8-42f5-ac62-3e83d4408bda",
                    "identifier": "3131313"
                }
            ]
        }
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        identifier = organization.identifiers.language("en").get(id="2d3b8d2c-77b8-42f5-ac62-3e83d4408bda")
        self.assertEqual(identifier.identifier, "3131313")

    def test_create_organization_contact_details_serializer(self):
        data = {
            "contact_details": [
                {
                    "value": "01234567",
                    "label": "myphone",
                    "note": "my phone",
                    "type": "phone",
                    "valid_from": "2015-01-01",
                    "valid_until": "2020-01-01",
                }
            ]
        }
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        contact = organization.contact_details.language("en").get(label="myphone")
        self.assertEqual(contact.value, "01234567")

    def test_update_organization_contact_details_serializer(self):
        data = {
            "contact_details": [
                {
                    "id": "651da7cd-f109-4aaa-b04c-df835fb6831f",
                    "value": "01291231321"
                }
            ]
        }
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        contact = organization.contact_details.language("en").get(id="651da7cd-f109-4aaa-b04c-df835fb6831f")
        self.assertEqual(contact.value, "01291231321")

    def test_create_organization_link_serializer(self):
        data = {
            "links": [
                {
                    "url": "http://google.com",
                    "note": "Just a link"
                }
            ]
        }
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        link = organization.links.language("en").get(url="http://google.com")
        self.assertEqual(link.note, "Just a link")

    def test_update_organization_link_serializer(self):
        data = {
            "links": [
                {
                    "id": "45b0a790-8c9e-4553-844b-431ed34b6b12",
                    "note": "github page of our member"
                }
            ]
        }

        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")

        link = organization.links.language("en").get(id="45b0a790-8c9e-4553-844b-431ed34b6b12")
        self.assertEqual(link.note, "github page of our member")

    def test_create_organization_othername_citation_serializer(self):
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
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        other_name = organization.other_names.language("en").get(id="53a22b00-1383-4bf5-b4be-4753d8d16062")
        link = other_name.links.language("en").get(url="http://google.com")
        self.assertEqual(link.url, "http://google.com")

    def test_update_organization_othername_citation_serializer(self):
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
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        other_name = organization.other_names.language("en").get(id="53a22b00-1383-4bf5-b4be-4753d8d16062")
        link = other_name.links.language("en").get(id="fe662497-c24d-4bbb-a72d-feb77319782a")
        self.assertEqual(link.note, "Just a link")
        self.assertEqual(link.field, "name")

    def test_create_organization_identifier_citation_serializer(self):
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
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        identifier = organization.identifiers.language("en").get(id="2d3b8d2c-77b8-42f5-ac62-3e83d4408bda")
        link = identifier.links.language("en").get(url="http://google.com")
        self.assertEqual(link.url, "http://google.com")

    def test_update_organization_identifier_citation_serializer(self):
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
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        identifier = organization.identifiers.language("en").get(id="2d3b8d2c-77b8-42f5-ac62-3e83d4408bda")
        link = identifier.links.language("en").get(id="02369098-7b46-4d62-9318-a5f1c2d385bd")
        self.assertEqual(link.note, "Just a link")

    def test_create_organization_contact_citation_serializer(self):
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
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        contact = organization.contact_details.language("en").get(id="651da7cd-f109-4aaa-b04c-df835fb6831f")
        link = contact.links.language("en").get(url="http://google.com")
        self.assertEqual(link.url, "http://google.com")

    def test_update_organization_contact_citation_serializer(self):
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

        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        contact = organization.contact_details.language("en").get(id="651da7cd-f109-4aaa-b04c-df835fb6831f")
        link = contact.links.language("en").get(id="26b8aa4b-2011-493d-bd74-e5e2d6ccd7cf")
        self.assertEqual(link.note, "yet another link")

    def test_create_organization_invalid_date(self):
        data = {
            "name": "acme corp",
            "founding_date": "invalid date",
            "dissolution_date": "invalid date",
        }
        serializer = OrganizationSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_create_organization_valid_date(self):
        data = {
            "name": "acme corp",
            "founding_date": "2015-01-01",
            "dissolution_date": "2015-01-01",
        }
        serializer = OrganizationSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})

    def test_create_organization_parent_not_exist(self):
        data = {
            "name": "acme corp",
            "parent_id": "not exist"
        }
        serializer = OrganizationSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_create_organization_parent_exist(self):
        data = {
            "name": "acme corp",
            "parent_id": "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3"
        }
        serializer = OrganizationSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})

    def test_create_organization_area_id_not_exist(self):
        data = {
            "name": "acme corp",
            "area_id": "does not exist"
        }
        serializer = OrganizationSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_create_organization_translated(self):
        data = {
            "name": "acme sdn bhd",
        }

        serializer = OrganizationSerializer(data=data, language="ms")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()

        organization = Organization.objects.language("ms").get(name="acme sdn bhd")
        self.assertEqual(organization.name, "acme sdn bhd")

    def test_update_organization_authorized_translated(self):
        data = {
            "abstract": "Cawangan KL Parti Lanun Malaysia"
        }
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        self.assertEqual(organization.abstract, "Cawangan KL Parti Lanun Malaysia")

    def test_fetch_organization_membership_translated(self):
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        organization_serializer = OrganizationSerializer(organization, language="ms")

        data = organization_serializer.data

        for membership in data["memberships"]:
            self.assertEqual(membership["language_code"], "ms")

    def test_fetch_organization_membership_post_translated(self):
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        organization_serializer = OrganizationSerializer(organization, language="ms")

        data = organization_serializer.data

        for membership in data["memberships"]:
            if membership["post"]:
                self.assertEqual(membership["post"]["language_code"], "ms")

    def test_fetch_organization_membership_person_translated(self):
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        organization_serializer = OrganizationSerializer(organization, language="ms")

        data = organization_serializer.data

        for membership in data["memberships"]:
            self.assertEqual(membership["person"]["language_code"], "ms")

    def test_fetch_organization_post_translated(self):
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        organization_serializer = OrganizationSerializer(organization, language="ms")
        data = organization_serializer.data
        for post in data["posts"]:
            self.assertEqual(post["language_code"], "ms")

    def test_fetch_organization_parent_translated(self):
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        organization_serializer = OrganizationSerializer(organization, language="ms")
        data = organization_serializer.data

        self.assertEqual(data["parent"]["language_code"], "ms")

    def test_fetch_organization_parent_othername_translated(self):
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        organization_serializer = OrganizationSerializer(organization, language="ms")
        data = organization_serializer.data

        # If translated doesn't exist the list will be empty, thus false. This is to make sure translation is fetch
        self.assertTrue(data["parent"]["other_names"])

        for other_name in data["parent"]["other_names"]:
            self.assertEqual(other_name["language_code"], "ms")

    def test_fetch_organization_parent_contactdetails_translated(self):
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        organization_serializer = OrganizationSerializer(organization, language="ms")
        data = organization_serializer.data

        # If translated doesn't exist the list will be empty, thus false. This is to make sure translation is fetch
        self.assertTrue(data["parent"]["contact_details"])
        for other_name in data["parent"]["contact_details"]:
            self.assertEqual(other_name["language_code"], "ms")

    def test_fetch_organization_parent_identifiers_translated(self):
        organization = Organization.objects.untranslated().get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        organization_serializer = OrganizationSerializer(organization, language="ms")
        data = organization_serializer.data
        self.assertTrue(data["parent"]["identifiers"])
        for identifier in data["parent"]["identifiers"]:
            self.assertEqual(identifier["language_code"], "ms")