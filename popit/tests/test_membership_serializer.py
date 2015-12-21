from django.test import TestCase
from popit.serializers import MembershipSerializer
from popit.models import Membership
from popit.models import ContactDetail
from popit.models import Link
from popit.signals.handlers import *
from popit.models import *
import logging


class MembershipSerializerTestCase(TestCase):

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

    def test_fetch_membership_serializer(self):
        membership = Membership.objects.untranslated().get(id="0a44195b-c3c9-4040-8dbf-be1aa250b700")
        serializer = MembershipSerializer(membership, language="en")
        data = serializer.data
        self.assertEqual(data["person"]["id"], "ab1a5788e5bae955c048748fa6af0e97")

    def test_create_membership_with_organization_serializer(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec"
        }

        serializer = MembershipSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        membership = Membership.objects.language("en").get(label="test membership")
        self.assertEqual(membership.person_id, "8497ba86-7485-42d2-9596-2ab14520f1f4")

    def test_create_membership_with_post_serializer(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "post_id": "c1f0f86b-a491-4986-b48d-861b58a3ef6e"
        }
        serializer = MembershipSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        membership = Membership.objects.language("en").get(label="test membership")
        self.assertEqual(membership.person_id, "8497ba86-7485-42d2-9596-2ab14520f1f4")

    def test_create_membership_without_post_and_organization(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
        }
        serializer = MembershipSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_create_membership_post_organization_conflict(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec",
            "post_id": "c1f0f86b-a491-4986-b48d-861b58a3ef6e"
        }
        serializer = MembershipSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_update_membership_serializer(self):
        data = {
            "label": "sweemeng land lubber"
        }
        membership = Membership.objects.untranslated().get(id="0a44195b-c3c9-4040-8dbf-be1aa250b700")
        serializer = MembershipSerializer(membership, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        membership = Membership.objects.language("en").get(id="0a44195b-c3c9-4040-8dbf-be1aa250b700")
        self.assertEqual(membership.label, "sweemeng land lubber")

    def test_update_membership_post_organization_conflict_serializer(self):
        data = {
            "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec"
        }

        membership = Membership.objects.untranslated().get(id="0a44195b-c3c9-4040-8dbf-be1aa250b700")
        logging.warn("Membership rorg id %s" % membership.post.organization_id)
        logging.warn("Data org id %s" % data["organization_id"])

        serializer = MembershipSerializer(membership, data=data, partial=True, language="en")
        serializer.is_valid()

        self.assertNotEqual(serializer.errors, {})

    def test_update_membership_organization_post_conflict_serializer(self):
        data = {
            "post_id":"3eb967bb-23e3-41b6-8cba-54aadac8d918"
        }
        membership = Membership.objects.untranslated().get(id="b351cdc2-6961-4fc7-9d61-08fca66e1d44")
        serializer = MembershipSerializer(membership, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_update_membership_update_contact_serializer(self):
        data = {
            "contact_details": [
                {
                    "id": "78a35135-52e3-4af9-8c32-ea3f557354fd",
                    "label": "captain's email"
                }
            ]
        }
        membership = Membership.objects.untranslated().get(id="b351cdc2-6961-4fc7-9d61-08fca66e1d44")
        serializer = MembershipSerializer(membership, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        contact = ContactDetail.objects.language("en").get(id="78a35135-52e3-4af9-8c32-ea3f557354fd")
        self.assertEqual(contact.label, "captain's email")

    def test_update_membership_create_contact_serializer(self):
        data = {
            "contact_details": [
                {
                    "type": "phone",
                    "value": "755-2525",
                    "label": "captain's phone"
                }
            ]
        }
        membership = Membership.objects.untranslated().get(id="b351cdc2-6961-4fc7-9d61-08fca66e1d44")
        serializer = MembershipSerializer(membership, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        contact = ContactDetail.objects.language("en").get(label="captain's phone")
        self.assertEqual(contact.label, "captain's phone")

    def test_update_membership_create_link_serializer(self):
        data = {
            "links": [
                {
                    "url": "http://thecaptain.tumblr.com",
                    "label": "Captain's Tumblr"
                }
            ]
        }
        membership = Membership.objects.untranslated().get(id="b351cdc2-6961-4fc7-9d61-08fca66e1d44")
        serializer = MembershipSerializer(membership, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        link = Link.objects.language("en").get(label="Captain's Tumblr")
        self.assertEqual(link.url, "http://thecaptain.tumblr.com")

    def test_update_membership_update_link_serializer(self):
        data = {
            "links": [
                {
                    "id": "239edef4-af68-4ffb-adce-96d17cbea79d",
                    "label": "Captain's page"
                }
            ]
        }
        membership = Membership.objects.untranslated().get(id="b351cdc2-6961-4fc7-9d61-08fca66e1d44")
        serializer = MembershipSerializer(membership, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        link = Link.objects.language("en").get(id="239edef4-af68-4ffb-adce-96d17cbea79d")
        self.assertEqual(link.label, "Captain's page")

    def test_update_membership_contact_citation_serializer(self):
        data = {
            "contact_details": [
                {

                    "id": "78a35135-52e3-4af9-8c32-ea3f557354fd",
                    "links": [
                        {
                            "id": "adebb549-e7a0-4ba6-a9ff-60eb2656c15b",
                            "label": "contact link"
                        }
                    ]

                }
            ]
        }
        membership = Membership.objects.untranslated().get(id="b351cdc2-6961-4fc7-9d61-08fca66e1d44")
        serializer = MembershipSerializer(membership, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        contacts = membership.contact_details.language('en').get(id="78a35135-52e3-4af9-8c32-ea3f557354fd")
        link = contacts.links.language("en").get(id="adebb549-e7a0-4ba6-a9ff-60eb2656c15b")
        self.assertEqual(link.label, "contact link")

    def test_create_membership_invalid_date(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec",
            "start_date": "invalid date",
            "end_date": "invalid date",
        }

        serializer = MembershipSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_create_membership_valid_date(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec",
            "start_date": "2010-01-01",
            "end_date": "2015-01-01",
        }

        serializer = MembershipSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})

    def test_create_membership_invalid_organization(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "organization_id": "not_exist",
        }

        serializer = MembershipSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_create_membership_invalid_person(self):
        data = {
            "label": "test membership",
            "person_id":"not_exist",
            "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec",
        }

        serializer = MembershipSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_create_membership_invalid_post(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec",
            "post_id": "not_exist"
        }
        serializer = MembershipSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_create_membership_invalid_area_id(self):
        data = {
            "label": "test membership",
            "person_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
            "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec",
            "area_id": "not_exist"
        }
        serializer = MembershipSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_create_membership_invalid_person_id_serializer(self):
        data = {
            "label": "test membership",
            "person_id":"does not exist",
            "organization_id": "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec",
            "start_date": "2010-01-01",
            "end_date": "2015-01-01"
        }
        serializer = MembershipSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})