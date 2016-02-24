__author__ = 'sweemeng'
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from django.test import TestCase
from popit.models import Person
from popit.models import Link
from popit.models import Contact
from popit.models import Identifier
from popit.models import OtherName
from popit.models import Area
from popit.serializers import LinkSerializer
from popit.serializers import OtherNameSerializer
from popit.serializers import IdentifierSerializer
from popit.serializers import ContactDetailSerializer
from popit.serializers import AreaSerializer
from popit.serializers.exceptions import ContentObjectNotAvailable
from popit.signals.handlers import *
from popit.models import *


class LinkSerializerTestCase(TestCase):

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
        post_save.disconnect(othername_save_handler, OtherName)
        post_delete.disconnect(othername_delete_handler, OtherName)
        post_save.disconnect(identifier_save_handler, Identifier)
        post_delete.disconnect(identifier_delete_handler, Identifier)
        post_save.disconnect(contactdetail_save_handler, ContactDetail)
        post_delete.disconnect(contactdetail_delete_handler, ContactDetail)
        post_save.disconnect(link_save_handler, Link)
        post_delete.disconnect(link_delete_handler, Link)

    def tearDown(self):
        post_save.connect(person_save_handler, Person)
        pre_delete.connect(person_delete_handler, Person)
        post_save.connect(organization_save_handler, Organization)
        pre_delete.connect(organization_delete_handler, Organization)
        post_save.connect(membership_save_handler, Membership)
        pre_delete.connect(membership_delete_handler, Membership)
        post_save.connect(post_save_handler, Post)
        pre_delete.connect(post_delete_handler, Post)
        post_save.connect(othername_save_handler, OtherName)
        post_delete.connect(othername_delete_handler, OtherName)
        post_save.connect(identifier_save_handler, Identifier)
        post_delete.connect(identifier_delete_handler, Identifier)
        post_save.connect(contactdetail_save_handler, ContactDetail)
        post_delete.connect(contactdetail_delete_handler, ContactDetail)
        post_save.connect(link_save_handler, Link)
        post_delete.connect(link_delete_handler, Link)

    def test_view_links_single(self):
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        url = person.links.untranslated().get(id="a4ffa24a9ef3cbcb8cfaa178c9329367")
        serializer = LinkSerializer(url, language="en")
        self.assertEqual(serializer.data["url"], "http://github.com/sweemeng/")

    def test_view_links_many(self):
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        url = person.links.untranslated().all()
        serializer = LinkSerializer(url, many=True, language="en")
        # TODO: This will fail, find out the exact data
        self.assertEqual(len(serializer.data), 2)

    def test_create_links(self):
        data = {
            "url": "http://twitter.com/sweemeng",
        }

        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')

        serializer = LinkSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save(content_object=person)

        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        url = person_.links.language("en").get(url="http://twitter.com/sweemeng")
        self.assertEqual(url.url, "http://twitter.com/sweemeng")

    def test_create_without_parent(self):
        data = {
            "url": "http://twitter.com/sweemeng",
        }

        serializer = LinkSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        with self.assertRaises(ContentObjectNotAvailable):
            serializer.save()

    def test_update_links(self):
        data = {
            "id": "a4ffa24a9ef3cbcb8cfaa178c9329367",
            "note": "just a random repo"
        }
        link = Link.objects.untranslated().get(id="a4ffa24a9ef3cbcb8cfaa178c9329367")
        serializer = LinkSerializer(link, data=data, partial=True, language='en')
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()

        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        url = person.links.language("en").get(id="a4ffa24a9ef3cbcb8cfaa178c9329367")
        self.assertEqual(url.note, "just a random repo")


class OtherNameSerializerTestCase(TestCase):

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
        post_save.disconnect(othername_save_handler, OtherName)
        post_delete.disconnect(othername_delete_handler, OtherName)
        post_save.disconnect(identifier_save_handler, Identifier)
        post_delete.disconnect(identifier_delete_handler, Identifier)
        post_save.disconnect(contactdetail_save_handler, ContactDetail)
        post_delete.disconnect(contactdetail_delete_handler, ContactDetail)
        post_save.disconnect(link_save_handler, Link)
        post_delete.disconnect(link_delete_handler, Link)

    def tearDown(self):
        post_save.connect(person_save_handler, Person)
        pre_delete.connect(person_delete_handler, Person)
        post_save.connect(organization_save_handler, Organization)
        pre_delete.connect(organization_delete_handler, Organization)
        post_save.connect(membership_save_handler, Membership)
        pre_delete.connect(membership_delete_handler, Membership)
        post_save.connect(post_save_handler, Post)
        pre_delete.connect(post_delete_handler, Post)
        post_save.connect(othername_save_handler, OtherName)
        post_delete.connect(othername_delete_handler, OtherName)
        post_save.connect(identifier_save_handler, Identifier)
        post_delete.connect(identifier_delete_handler, Identifier)
        post_save.connect(contactdetail_save_handler, ContactDetail)
        post_delete.connect(contactdetail_delete_handler, ContactDetail)
        post_save.connect(link_save_handler, Link)
        post_delete.connect(link_delete_handler, Link)

    def test_view_othername_list(self):
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        other_names = person.other_names.untranslated().all()
        serializer = OtherNameSerializer(other_names, many=True, language="en")
        self.assertEqual(len(serializer.data), 1)
        self.assertEqual(serializer.data[0]["name"], "Jane")

    def test_view_othername_single(self):
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        other_names = person.other_names.untranslated().get(id="cf93e73f-91b6-4fad-bf76-0782c80297a8")
        serializer = OtherNameSerializer(other_names, language="en")
        self.assertEqual(serializer.data["name"], "Jane")

    def test_create_othername(self):
        data = {
            "name": "jane",
            "family_name": "jambul",
            "given_name": "test person",
            "start_date": "1950-01-01",
            "end_date": "2010-01-01",
        }
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        serializer = OtherNameSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save(content_object=person)

        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        other_name = person_.other_names.language('en').get(name="jane")
        self.assertEqual(other_name.given_name, "test person")

    def test_create_othername_without_parent(self):
        data = {
            "name": "jane",
            "family_name": "jambul",
            "given_name": "test person",
            "start_date": "1950-01-01",
            "end_date": "2010-01-01",
        }
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        serializer = OtherNameSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        with self.assertRaises(ContentObjectNotAvailable):
            serializer.save()

    def test_update_othername(self):
        data = {
            "family_name": "jambul",
        }
        person = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        other_name = person.other_names.language('en').get(id="cf93e73f-91b6-4fad-bf76-0782c80297a8")
        serializer = OtherNameSerializer(other_name, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save(content_object=person)
        other_name_ = OtherName.objects.language("en").get(id="cf93e73f-91b6-4fad-bf76-0782c80297a8")
        self.assertEqual(other_name_.family_name, "jambul")


class IdentifierSerializerTestCase(TestCase):

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
        post_save.disconnect(othername_save_handler, OtherName)
        post_delete.disconnect(othername_delete_handler, OtherName)
        post_save.disconnect(identifier_save_handler, Identifier)
        post_delete.disconnect(identifier_delete_handler, Identifier)
        post_save.disconnect(contactdetail_save_handler, ContactDetail)
        post_delete.disconnect(contactdetail_delete_handler, ContactDetail)
        post_save.disconnect(link_save_handler, Link)
        post_delete.disconnect(link_delete_handler, Link)

    def tearDown(self):
        post_save.connect(person_save_handler, Person)
        pre_delete.connect(person_delete_handler, Person)
        post_save.connect(organization_save_handler, Organization)
        pre_delete.connect(organization_delete_handler, Organization)
        post_save.connect(membership_save_handler, Membership)
        pre_delete.connect(membership_delete_handler, Membership)
        post_save.connect(post_save_handler, Post)
        pre_delete.connect(post_delete_handler, Post)
        post_save.connect(othername_save_handler, OtherName)
        post_delete.connect(othername_delete_handler, OtherName)
        post_save.connect(identifier_save_handler, Identifier)
        post_delete.connect(identifier_delete_handler, Identifier)
        post_save.connect(contactdetail_save_handler, ContactDetail)
        post_delete.connect(contactdetail_delete_handler, ContactDetail)
        post_save.connect(link_save_handler, Link)
        post_delete.connect(link_delete_handler, Link)

    def test_view_identifier_list(self):
        person = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        identifiers = person.identifiers.untranslated().all()
        serializer = IdentifierSerializer(identifiers, many=True, language="en")
        self.assertEqual(len(serializer.data), 2)

    def test_view_identifier_single(self):
        person = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        identifiers = person.identifiers.untranslated().get(id="34b59cb9-607a-43c7-9d13-dfe258790ebf")
        serializer = IdentifierSerializer(identifiers, language="en")
        self.assertEqual(serializer.data["identifier"], "53110321")

    def test_create_identifier_without_parent(self):
        data = {
            "scheme": "IC",
            "identifier": "129031309",
        }
        serializer = IdentifierSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        with self.assertRaises(ContentObjectNotAvailable):
            serializer.save()

    def test_create_identifier(self):
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        data = {
            "scheme": "IC",
            "identifier": "129031309",
        }
        serializer = IdentifierSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save(content_object=person)

        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')

        identifier = person_.identifiers.language('en').get(identifier="129031309")
        self.assertEqual(identifier.scheme, "IC")

    def test_update_identifier(self):
        data = {
            "identifier": "53110322",
        }
        person = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        identifier = person.identifiers.language("en").get(id="34b59cb9-607a-43c7-9d13-dfe258790ebf")
        serializer = IdentifierSerializer(identifier, data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()

        person_ = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        identifier = person_.identifiers.language('en').get(id="34b59cb9-607a-43c7-9d13-dfe258790ebf")
        self.assertEqual(identifier.identifier, '53110322')




class PersonContactSerializerTestCase(TestCase):

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
        post_save.disconnect(othername_save_handler, OtherName)
        post_delete.disconnect(othername_delete_handler, OtherName)
        post_save.disconnect(identifier_save_handler, Identifier)
        post_delete.disconnect(identifier_delete_handler, Identifier)
        post_save.disconnect(contactdetail_save_handler, ContactDetail)
        post_delete.disconnect(contactdetail_delete_handler, ContactDetail)
        post_save.disconnect(link_save_handler, Link)
        post_delete.disconnect(link_delete_handler, Link)

    def tearDown(self):
        post_save.connect(person_save_handler, Person)
        pre_delete.connect(person_delete_handler, Person)
        post_save.connect(organization_save_handler, Organization)
        pre_delete.connect(organization_delete_handler, Organization)
        post_save.connect(membership_save_handler, Membership)
        pre_delete.connect(membership_delete_handler, Membership)
        post_save.connect(post_save_handler, Post)
        pre_delete.connect(post_delete_handler, Post)
        post_save.connect(othername_save_handler, OtherName)
        post_delete.connect(othername_delete_handler, OtherName)
        post_save.connect(identifier_save_handler, Identifier)
        post_delete.connect(identifier_delete_handler, Identifier)
        post_save.connect(contactdetail_save_handler, ContactDetail)
        post_delete.connect(contactdetail_delete_handler, ContactDetail)
        post_save.connect(link_save_handler, Link)
        post_delete.connect(link_delete_handler, Link)

    def test_view_contact_details_list(self):
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        contact_details = person.contact_details.untranslated().all()
        serializers = ContactDetailSerializer(contact_details, language="en", many=True)
        self.assertEqual(len(serializers.data), 1)
        self.assertEqual(serializers.data[0]["value"], "0123421221")

    def test_view_contact_details(self):
        # a66cb422-eec3-4861-bae1-a64ae5dbde61
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')

        contact_details = person.contact_details.untranslated().get(id="a66cb422-eec3-4861-bae1-a64ae5dbde61")
        serializer = ContactDetailSerializer(contact_details, language="en")
        self.assertEqual(serializer.data["value"], "0123421221")

    def test_create_contact_details(self):
        data = {
            "type":"twitter",
            "value": "sinarproject",
        }
        person = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        serializer = ContactDetailSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save(content_object=person)
        person_ = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        contact_details = person_.contact_details.language('en').get(type="twitter")
        self.assertEqual(contact_details.value, "sinarproject")

    def test_create_contact_details_without_parent(self):
        data = {
            "type":"twitter",
            "value": "sinarproject",
        }

        serializer = ContactDetailSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        with self.assertRaises(ContentObjectNotAvailable):
            serializer.save()

    def test_test_update_contact_details(self):
        data = {
            "id": "a66cb422-eec3-4861-bae1-a64ae5dbde61",
            "value": "0123421222",
        }

        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')

        contact_details = person.contact_details.untranslated().get(id="a66cb422-eec3-4861-bae1-a64ae5dbde61")
        serializer = ContactDetailSerializer(contact_details, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()

        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        contact_details = person_.contact_details.language('en').get(id="a66cb422-eec3-4861-bae1-a64ae5dbde61")
        self.assertEqual(contact_details.value, "0123421222")


class AreaSerializerTestCase(TestCase):

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
        post_save.disconnect(othername_save_handler, OtherName)
        post_delete.disconnect(othername_delete_handler, OtherName)
        post_save.disconnect(identifier_save_handler, Identifier)
        post_delete.disconnect(identifier_delete_handler, Identifier)
        post_save.disconnect(contactdetail_save_handler, ContactDetail)
        post_delete.disconnect(contactdetail_delete_handler, ContactDetail)
        post_save.disconnect(link_save_handler, Link)
        post_delete.disconnect(link_delete_handler, Link)

    def tearDown(self):
        post_save.connect(person_save_handler, Person)
        pre_delete.connect(person_delete_handler, Person)
        post_save.connect(organization_save_handler, Organization)
        pre_delete.connect(organization_delete_handler, Organization)
        post_save.connect(membership_save_handler, Membership)
        pre_delete.connect(membership_delete_handler, Membership)
        post_save.connect(post_save_handler, Post)
        pre_delete.connect(post_delete_handler, Post)
        post_save.connect(othername_save_handler, OtherName)
        post_delete.connect(othername_delete_handler, OtherName)
        post_save.connect(identifier_save_handler, Identifier)
        post_delete.connect(identifier_delete_handler, Identifier)
        post_save.connect(contactdetail_save_handler, ContactDetail)
        post_delete.connect(contactdetail_delete_handler, ContactDetail)
        post_save.connect(link_save_handler, Link)
        post_delete.connect(link_delete_handler, Link)

    def test_list_area(self):
        area = Area.objects.language("en").all()
        print area
        serializer = AreaSerializer(area, language="en", many=True)
        self.assertEqual(len(serializer.data), 2)

    def test_view_area(self):
        area = Area.objects.language("en").get(id="640c0f1d-2305-4d17-97fe-6aa59f079cc4")
        serializer = AreaSerializer(area, language="en")
        self.assertEqual(serializer.data["name"], "kuala lumpur")

    def test_create_area(self):
        data = {
            "name": "timbuktu"
        }
        serializer = AreaSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})

        serializer.save()
        area = Area.objects.language("en").get(name="timbuktu")
        # Just to proof that it save into database
        self.assertEqual(area.name, "timbuktu")

    def test_update_area(self):
        data = {
            "classification": "city"
        }
        area = Area.objects.untranslated().get(id="640c0f1d-2305-4d17-97fe-6aa59f079cc4")
        serializer = AreaSerializer(area, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        area = Area.objects.language("en").get(id="640c0f1d-2305-4d17-97fe-6aa59f079cc4")
        self.assertEqual(area.classification, "city")

    def test_create_area_link(self):
        data = {
            "classification": "city",
            "links": [
                {
                    "url": "http://www.google.com",
                    "note": "just a link"
                }
            ]
        }
        area = Area.objects.untranslated().get(id="640c0f1d-2305-4d17-97fe-6aa59f079cc4")
        serializer = AreaSerializer(area, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        link = area.links.language("en").get(url="http://www.google.com")
        self.assertEqual(link.note, "just a link")

    def test_update_area_link(self):
        data = {

            "links": [
                {
                    "id": "ed8a52d8-5503-45aa-a2ad-9931461172d2",
                    "note": "just a link"
                }

            ]
        }
        area = Area.objects.untranslated().get(id="640c0f1d-2305-4d17-97fe-6aa59f079cc4")
        serializer = AreaSerializer(area, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        link = area.links.language("en").get(id="ed8a52d8-5503-45aa-a2ad-9931461172d2")
        self.assertEqual(link.note, "just a link")