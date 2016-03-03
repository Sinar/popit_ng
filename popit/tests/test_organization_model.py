__author__ = 'sweemeng'
from django.test import TestCase
from django.core.exceptions import ValidationError
from popit.models import Organization
from popit.models import OtherName
from popit.models import Link
from popit.models import Identifier
from popit.models import ContactDetail
from popit.models import Area
from popit.models.exception import PopItFieldNotExist
from popit.signals.handlers import *
from popit.models import *


# This mostly server as examples
# TODO: Add test for setting parent org
class OrganizationTestCase(TestCase):

    fixtures = [ "api_request_test_data.yaml" ]

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

    def test_create_organization_minimum_field(self):
        organization = Organization.objects.language("en").create(
            name="acme corp"
        )
        organization_ = Organization.objects.language("en").get(name="acme corp")
        self.assertEqual(organization_.name, "acme corp")

    def test_create_organization(self):
        Organization.objects.language("en").create(
            name="acme corp",
            classification="corporation",
            abstract="sell useless object",
            description="sell useless object to coyote to hunt roadrunner",
            founding_date="1902-01-01",
            dissolution_date="2020-01-01"
        )
        organization = Organization.objects.language("en").get(name="acme corp")
        self.assertEqual(organization.classification, "corporation")

    def test_create_organization_other_name(self):
        organization = Organization.objects.language("en").create(
            name="acme corp"
        )
        OtherName.objects.language("en").create(
            name="evil corp",
            content_object = organization,
            note="e-corp"
        )
        organization_ = Organization.objects.language("en").get(name="acme corp")
        other_name = organization_.other_names.language("en").get(name="evil corp")
        self.assertEqual(other_name.note, "e-corp")

    def test_create_organization_link(self):
        organization = Organization.objects.language("en").create(
            name="acme corp"
        )
        Link.objects.language("en").create(
            url="http://google.com",
            note="Some url",
            content_object=organization
        )

        organization_ = Organization.objects.language("en").get(name="acme corp")
        link = organization_.links.language("en").get(url="http://google.com")
        self.assertEqual(link.note, "Some url")

    def test_create_organization_identifier(self):
        organization = Organization.objects.language("en").create(
            name="acme corp"
        )

        Identifier.objects.language("en").create(
            identifier="12121231",
            scheme="ssm",
            content_object=organization
        )

        organization_ = Organization.objects.language("en").get(name="acme corp")
        identifier = organization_.identifiers.language("en").get(identifier="12121231")
        self.assertEqual(identifier.scheme, "ssm")

    def test_create_organization_contact(self):
        organization = Organization.objects.language("en").create(
            name="acme corp"
        )
        ContactDetail.objects.language("en").create(
            type='phone',
            value='01234567',
            label='myphone',
            note='my phone',
            valid_from="2015-01-01",
            valid_until="2020-01-01",
            content_object=organization
        )

        organization_ = Organization.objects.language("en").get(name="acme corp")
        contact = organization_.contact_details.language("en").get(value="01234567")
        self.assertEqual(contact.type, "phone")

    def test_create_organization_area(self):
        area = Area.objects.language("en").get(name="kuala lumpur")
        Organization.objects.language("en").create(
            name="acme corp",
            area=area
        )
        organization = Organization.objects.language("en").get(name="acme corp")
        self.assertEqual(organization.area, area)

    def test_create_organization_citation(self):
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        organization.add_citation("name", "http://pirateparty.com", "just a link")

        organization_ = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        links=organization_.links.get(field="name")
        self.assertEqual(links.url, "http://pirateparty.com")

    def test_create_organization_other_name_citation(self):
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        other_name = organization.other_names.language("en").get(id="53a22b00-1383-4bf5-b4be-4753d8d16062")
        other_name.add_citation("family_name", "http://sinarproject.org", "just another note")
        organization_ = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        other_name = organization_.other_names.language("en").get(id="53a22b00-1383-4bf5-b4be-4753d8d16062")
        link = other_name.links.language("en").get(field="family_name")
        self.assertEqual(link.url, "http://sinarproject.org")

    def test_create_organization_identifier_citation(self):
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        identifier = organization.identifiers.get(id="2d3b8d2c-77b8-42f5-ac62-3e83d4408bda")
        identifier.add_citation("scheme", "http://sinarproject.org", "random source")
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        identifier = organization.identifiers.language("en").get(id="2d3b8d2c-77b8-42f5-ac62-3e83d4408bda")
        link = identifier.links.language("en").get(field="scheme")
        self.assertEqual(link.url, "http://sinarproject.org")

    def test_create_organization_contact_citation(self):
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        contact = organization.contact_details.language("en").get(id="651da7cd-f109-4aaa-b04c-df835fb6831f")
        contact.add_citation("value","http://google.com", "find it")

        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        contact = organization.contact_details.language("en").get(id="651da7cd-f109-4aaa-b04c-df835fb6831f")
        link = contact.links.language("en").get(field="value")
        self.assertEqual(link.url, "http://google.com")

    def test_create_organization_area_citation(self):
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        area = organization.area
        area.add_citation("name", "http://en.wikipedia.com", "wikipedia")
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        area = organization.area
        link = area.links.language("en").get(field="name")
        self.assertEqual(link.url, "http://en.wikipedia.com")

    # TODO: Add bad citation
    def test_create_organization_citation_citation_bad_field(self):
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        with self.assertRaises(PopItFieldNotExist):
            organization.add_citation("names", "pirateparty.com", "just a link")

    def test_create_organization_othername_bad_field(self):
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        other_name = organization.other_names.language("en").get(id="53a22b00-1383-4bf5-b4be-4753d8d16062")
        with self.assertRaises(PopItFieldNotExist):
            other_name.add_citation("nam", "sinarproject.org", "just another note")

    def test_create_organization_identifiers_citation_bad_field(self):
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        identifier = organization.identifiers.get(id="2d3b8d2c-77b8-42f5-ac62-3e83d4408bda")
        with self.assertRaises(PopItFieldNotExist):
            identifier.add_citation("name", "sinarproject.org", "random source")

    def test_create_organization_contact_citation_bad_field(self):
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        contact = organization.contact_details.language("en").get(id="651da7cd-f109-4aaa-b04c-df835fb6831f")
        with self.assertRaises(PopItFieldNotExist):
            contact.add_citation("name","google.com", "find it")

    def test_create_organization_area_citation_bad_field(self):
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        area = organization.area
        with self.assertRaises(PopItFieldNotExist):
            area.add_citation("names", "en.wikipedia.com", "wikipedia")

    def test_create_organization_invalid_date(self):
        with self.assertRaises(ValidationError):
            Organization.objects.language("en").create(
                name="acme corp",
                classification="corporation",
                abstract="sell useless object",
                description="sell useless object to coyote to hunt roadrunner",
                founding_date="abcd",
                dissolution_date="abcd"
            )
