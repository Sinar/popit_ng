__author__ = "sweemeng"
from django.test import TestCase
from rest_framework.test import APIRequestFactory
from popit.models import Person
from popit.models import Link
from popit.models import OtherName
from popit.models import ContactDetail
from popit.models import Identifier
from popit.models.exception import PopItFieldNotExist
from popit.signals.handlers import *
from popit.models import *


# Unit test only have to test for attribute
# The reason is a model should map into popolo standard, unittest is a good way to show that
class PersonTestCase(TestCase):

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

    def test_minimum_fields_to_create_person(self):
            # This is mostly to show people what is the required field

        person = Person.objects.language('en').create(
            name="John Doe"
        )
        # This is the minimum field needed to create a person
        # id should be automatically generated
        self.assertEqual(person.name, "John Doe")

    def test_create_person(self):
        # This is what the field look like if you add everything
        person = Person.objects.language('en').create(
            name="John",
            family_name="Doe",
            given_name="Harry",
            additional_name="The Fake",
            honorific_prefix="Sir",
            honorific_suffix="of Sinar Office",
            email="doe@sinarproject.org",
            gender="male",
            birth_date="1901-01-01",
            death_date="2001-01-01",
            image="",
            summary="This is a test person",
            biography="This is a test person in sinar project",
            national_identity="Malaysian"
        )

        person_ = Person.objects.language('en').get(name='John')
        # Do not assume that '' is true. Well it is, but the intention is not clear
        self.assertNotEqual(person_.id, '')
        self.assertEqual(person_.name, "John")

    # Each Test must be independent
    def test_create_person_other_name(self):
        person = Person.objects.language('en').create(
            name="John Doe"
        )
        other_name = OtherName.objects.language('en').create(
            name="Jane",
            family_name="Doe",
            additional_name="Before fake",
            content_object=person,
            note="Test Data"
        )
        person_ = Person.objects.language('en').get(name='John Doe')
        # The reason is, empty field is allowed into id field
        self.assertNotEqual(person_.id, '')
        other_names = person_.other_names.language('en').all()[0]
        self.assertEqual(other_names.name, "Jane")
        self.assertNotEqual(other_names.id, '')

    def test_create_person_identifiers(self):
        person = Person.objects.language('en').create(
            name="John Doe"
        )

        identifiers = Identifier.objects.language('en').create(
            identifier="12123123213",
            scheme="random",
            content_object=person
        )
        person_ = Person.objects.language('en').get(name='John Doe')
        self.assertNotEqual(person_.id, '')
        identifiers_ = person_.identifiers.language('en').all()[0]
        self.assertEqual(identifiers_.identifier, "12123123213")
        self.assertNotEqual(identifiers_.id, '')

    def test_create_person_contact_details(self):
        person = Person.objects.language('en').create(
            name="John Doe"
        )
        contact_details = ContactDetail.objects.language('en').create(
            type='phone',
            value='01234567',
            label='myphone',
            note='my phone',
            valid_from="2015-01-01",
            valid_until="2020-01-01",
            content_object=person
        )

        person_ = Person.objects.language('en').get(name='John Doe')
        self.assertNotEqual(person_.id, "")
        contact_details_ = person_.contact_details.language('en').all()[0]
        self.assertEqual(contact_details_.type, 'phone')
        self.assertNotEqual(contact_details_.id, '')

    def test_create_person_links(self):
        person = Person.objects.language('en').create(
            name="John Doe"
        )
        links = Link.objects.language('en').create(
            url="www.google.com",
            note="some link",
            content_object=person
        )

        person_ = Person.objects.language('en').get(name='John Doe')
        self.assertNotEqual(person_.id, '')
        links_ = person_.links.language('en').all()[0]
        self.assertNotEqual(links_.id, '')
        self.assertEqual(links_.url, 'www.google.com')

    def test_create_person_citation(self):
        person = Person.objects.language('en').create(
            name="john bin doe"
        )

        person_ = Person.objects.language('en').get(name='john bin doe')
        person_.add_citation('name', 'google.com', 'just a link')
        links = person_.links.language('en').filter(field='name')

        self.assertEqual(links[0].url, 'google.com')

    # Each citation is done on object level. This might be hard on the UI
    # But it is easier on data model. In Django Rest Framework, there is nested relationship, which show the full thing
    # Why I will use that? Friendly to caching. And using nested relationship require us to write a custom create and update method anyway
    def test_create_othername_citation(self):
        person = Person.objects.language('en').create(
            name='john jambul'
        )

        other_name = OtherName.objects.language('en').create(
            name="Joe",
            family_name="Jambul",
            content_object=person,
            note="Test Data"
        )
        other_name.add_citation('family_name', 'google.com', 'just search it')

        # I don't like this query. Can potentially slow down.
        person_ = Person.objects.language('en').get(name='john jambul')
        other_name_ = person_.other_names.language('en').all()
        links= other_name_[0].links.language('en').all()
        self.assertEqual(links[0].url, 'google.com')

    def test_create_contact_citation(self):
        person = Person.objects.language('en').create(
            name="John Doe"
        )
        contact_details = ContactDetail.objects.language('en').create(
            type='phone',
            value='01234567',
            label='myphone',
            note='my phone',
            valid_from="2015-01-01",
            valid_until="2020-01-01",
            content_object=person
        )

        contact_details.add_citation('type', 'google.com', 'just search it')

        person_ = Person.objects.language('en').get(name='John Doe')
        self.assertNotEqual(person_.id, "")
        contact_details_ = person_.contact_details.language('en').all()[0]
        links = contact_details_.links.language('en').all()
        self.assertEqual(links[0].url, 'google.com')

    def test_create_identifier_citation(self):
        person = Person.objects.language('en').create(
            name="John Doe"
        )

        identifiers = Identifier.objects.language('en').create(
            identifier="12123123213",
            scheme="random",
            content_object=person
        )

        identifiers.add_citation("identifier", 'google.com', 'just search it')

        person_ = Person.objects.language('en').get(name='John Doe')
        self.assertNotEqual(person_.id, '')
        identifiers_ = person_.identifiers.language('en').all()[0]
        links = identifiers_.links.language('en').all()

        self.assertEqual(links[0].url, 'google.com')

    def test_create_person_citation_field_not_exist(self):
        person = Person.objects.language('en').create(
            name="john bin doe"
        )

        person_ = Person.objects.language('en').get(name='john bin doe')
        with self.assertRaises(PopItFieldNotExist):
            person_.add_citation('species', 'google.com', 'just a link')

    def test_create_othername_citation_not_exist(self):
        person = Person.objects.language('en').create(
            name='john jambul'
        )

        other_name = OtherName.objects.language('en').create(
            name="Joe",
            family_name="Jambul",
            content_object=person,
            note="Test Data"
        )
        with self.assertRaises(PopItFieldNotExist):
            other_name.add_citation('species', 'google.com', 'just search it')

    def test_create_contact_citation_field_not_exist(self):
        person = Person.objects.language('en').create(
            name="John Doe"
        )
        contact_details = ContactDetail.objects.language('en').create(
            type='phone',
            value='01234567',
            label='myphone',
            note='my phone',
            valid_from="2015-01-01",
            valid_until="2020-01-01",
            content_object=person
        )

        with self.assertRaises(PopItFieldNotExist):
            contact_details.add_citation('handle', 'google.com', 'just search it')

    def test_create_identifier_citation_field_not_exist(self):
        person = Person.objects.language('en').create(
            name="John Doe"
        )

        identifiers = Identifier.objects.language('en').create(
            identifier="12123123213",
            scheme="random",
            content_object=person
        )
        with self.assertRaises(PopItFieldNotExist):
            identifiers.add_citation("code", 'google.com', 'just search it')

    def test_person_citation_exist(self):
        person = Person.objects.language('en').create(
            name="john bin doe"
        )

        person_ = Person.objects.language('en').get(name='john bin doe')
        person_.add_citation('name', 'google.com', 'just a link')
        self.assertTrue(person_.citation_exist('name'))

    def test_othername_citation_exist(self):
        person = Person.objects.language('en').create(
            name='john jambul'
        )

        other_name = OtherName.objects.language('en').create(
            name="Joe",
            family_name="Jambul",
            content_object=person,
            note="Test Data"
        )
        other_name.add_citation('family_name', 'google.com', 'just search it')

        # I don't like this query. Can potentially slow down.
        person_ = Person.objects.language('en').get(name='john jambul')
        other_name_ = person_.other_names.language('en').all()
        self.assertTrue(other_name_[0].citation_exist('family_name'))

    def test_contact_citation_exist(self):
        person = Person.objects.language('en').create(
            name="John Doe"
        )
        contact_details = ContactDetail.objects.language('en').create(
            type='phone',
            value='01234567',
            label='myphone',
            note='my phone',
            valid_from="2015-01-01",
            valid_until="2020-01-01",
            content_object=person
        )

        contact_details.add_citation('type', 'google.com', 'just search it')

        person_ = Person.objects.language('en').get(name='John Doe')
        self.assertNotEqual(person_.id, "")
        contact_details_ = person_.contact_details.language('en').all()[0]
        self.assertTrue(contact_details_.citation_exist('type'))

    def test_identifier_citation_exist(self):
        person = Person.objects.language('en').create(
            name="John Doe"
        )

        identifiers = Identifier.objects.language('en').create(
            identifier="12123123213",
            scheme="random",
            content_object=person
        )

        identifiers.add_citation("identifier", 'google.com', 'just search it')

        person_ = Person.objects.language('en').get(name='John Doe')
        self.assertNotEqual(person_.id, '')
        identifiers_ = person_.identifiers.language('en').all()[0]
        self.assertTrue(identifiers_.citation_exist('identifier'))

    def test_person_citation_not_exist(self):
        person = Person.objects.language('en').create(
            name="john bin doe"
        )

        person_ = Person.objects.language('en').get(name='john bin doe')

        self.assertFalse(person_.citation_exist('name'))

    def test_othername_citation_not_exist(self):
        person = Person.objects.language('en').create(
            name='john jambul'
        )

        other_name = OtherName.objects.language('en').create(
            name="Joe",
            family_name="Jambul",
            content_object=person,
            note="Test Data"
        )

        # I don't like this query. Can potentially slow down.
        person_ = Person.objects.language('en').get(name='john jambul')
        other_name_ = person_.other_names.language('en').all()
        self.assertFalse(other_name_[0].citation_exist('family_name'))

    def test_contact_citation_not_exist(self):
        person = Person.objects.language('en').create(
            name="John Doe"
        )
        contact_details = ContactDetail.objects.language('en').create(
            type='phone',
            value='01234567',
            label='myphone',
            note='my phone',
            valid_from="2015-01-01",
            valid_until="2020-01-01",
            content_object=person
        )

        person_ = Person.objects.language('en').get(name='John Doe')
        self.assertNotEqual(person_.id, "")
        contact_details_ = person_.contact_details.language('en').all()[0]
        self.assertFalse(contact_details_.citation_exist('type'))

    def test_identifier_citation_not_exist(self):
        person = Person.objects.language('en').create(
            name="John Doe"
        )

        identifiers = Identifier.objects.language('en').create(
            identifier="12123123213",
            scheme="random",
            content_object=person
        )

        person_ = Person.objects.language('en').get(name='John Doe')
        self.assertNotEqual(person_.id, '')
        identifiers_ = person_.identifiers.language('en').all()[0]
        self.assertFalse(identifiers_.citation_exist('identifier'))

    def test_field_type_correct_person(self):
        # I wonder if I can just take the json schema in popolo and verify it there :-/ - SM
        person = Person.objects.language('en').create(
            name="John",
            family_name="Doe",
            given_name="Harry",
            additional_name="The Fake",
            honorific_prefix="Sir",
            honorific_suffix="of Sinar Office",
            email="doe@sinarproject.org",
            gender="male",
            birth_date="1901-01-01",
            death_date="2001-01-01",
            image="",
            summary="This is a test person",
            biography="This is a test person in sinar project",
            national_identity="Malaysian"
        )

        self.assertEqual(type(person.name), str)
        self.assertEqual(type(person.family_name), str)
        self.assertEqual(type(person.given_name), str)
        self.assertEqual(type(person.additional_name), str)
        self.assertEqual(type(person.honorific_prefix), str)
        self.assertEqual(type(person.honorific_suffix), str)
        # This is a email, see if validator make sense
        self.assertEqual(type(person.email), str)
        self.assertEqual(type(person.gender), str)
        # There is validator in popolo
        self.assertEqual(type(person.birth_date), str)
        self.assertEqual(type(person.death_date), str)
        # this is a path
        self.assertEqual(type(person.image), str)
        self.assertEqual(type(person.summary), str)
        self.assertEqual(type(person.biography), str)
        self.assertEqual(type(person.national_identity), str)

    def test_field_type_correct_links(self):

        person = Person.objects.language('en').create(
            name="John Doe"
        )
        links = Link.objects.language('en').create(
            label="test data",
            field="",
            url="www.google.com",
            note="some link",
            content_object=person
        )

        self.assertEqual(type(links.label), str)
        self.assertEqual(type(links.field), str)
        self.assertEqual(type(links.url), str)
        self.assertEqual(type(links.note), str)

    def test_field_type_correct_othernames(self):
        person = Person.objects.language('en').create(
            name="John Doe"
        )
        other_name = OtherName.objects.language('en').create(
            name="Jane",
            family_name="Doe",
            given_name="fake person",
            additional_name="Before fake",
            honorific_prefix="Dato",
            honorific_suffix="of somewhere",
            patronymic_name="",
            start_date="2010-10-10",
            end_date="2011-10-10",
            content_object=person,
            note="Test Data"
        )

        self.assertEqual(type(other_name.name), str)
        self.assertEqual(type(other_name.family_name), str)
        self.assertEqual(type(other_name.given_name), str)
        self.assertEqual(type(other_name.additional_name), str)
        self.assertEqual(type(other_name.honorific_prefix), str)
        self.assertEqual(type(other_name.honorific_suffix), str)
        # Need validation in tthese
        self.assertEqual(type(other_name.start_date), str)
        self.assertEqual(type(other_name.end_date), str)
        self.assertEqual(type(other_name.note), str)

    def test_field_type_correct_identifier(self):
        person = Person.objects.language('en').create(
            name="John Doe"
        )

        identifiers = Identifier.objects.language('en').create(
            identifier="12123123213",
            scheme="random",
            content_object=person
        )

        self.assertEqual(type(identifiers.identifier), str)
        self.assertEqual(type(identifiers.scheme), str)

    def test_field_type_correct_contact_details(self):
        person = Person.objects.language('en').create(
            name="John Doe"
        )
        contact_details = ContactDetail.objects.language('en').create(
            type='phone',
            value='01234567',
            label='myphone',
            note='my phone',
            valid_from="2015-01-01",
            valid_until="2020-01-01",
            content_object=person
        )
        self.assertEqual(type(contact_details.type), str)
        self.assertEqual(type(contact_details.value), str)
        self.assertEqual(type(contact_details.label), str)
        self.assertEqual(type(contact_details.note), str)
        self.assertEqual(type(contact_details.valid_from), str)
        self.assertEqual(type(contact_details.valid_until), str)
