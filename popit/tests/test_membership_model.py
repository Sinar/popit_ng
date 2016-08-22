from django.core.exceptions import ValidationError
from popit.models import *
from popit.tests.base_testcase import BasePopitTestCase


class MembershipModelTestCase(BasePopitTestCase):

    def test_create_membership_with_organization(self):
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        organization = Organization.objects.language("en").get(id="e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec")
        membership = Membership.objects.language("en").create(
            person=person,
            organization=organization
        )
        self.assertEqual(membership.organization_id, "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec")

    def test_create_membership_with_post(self):
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        membership = Membership.objects.language("en").create(
            person=person,
            post=post
        )
        self.assertEqual(membership.post_id,"c1f0f86b-a491-4986-b48d-861b58a3ef6e")

    def test_create_membership_without_organization_or_post(self):
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        with self.assertRaises(ValidationError):
            Membership.objects.language("en").create(
                person=person
            )

    def test_create_membership_expected(self):
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        area = Area.objects.language("en").get(id="640c0f1d-2305-4d17-97fe-6aa59f079cc4")
        membership = Membership.objects.language("en").create(
            label="Test membership",
            start_date="2010-01-01",
            end_date="2016-01-01",
            person=person,
            organization=organization,
            post=post,
            area=area,
        )
        self.assertEqual(organization.id, "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")

    def test_create_membership_post_org_diff_organization(self):
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")

        organization = Organization.objects.language("en").get(id="e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec")
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        with self.assertRaises(ValidationError):
            Membership.objects.language("en").create(
                person=person,
                organization=organization,
                post=post
            )

    def test_create_membership_full(self):
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        area = Area.objects.language("en").get(id="640c0f1d-2305-4d17-97fe-6aa59f079cc4")
        on_behalf_of = Organization.objects.language("en").get(id="e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec")

        membership=Membership.objects.language("en").create(
            label="Test full membership",
            start_date="2010-01-01",
            end_date="2016-01-01",
            person=person,
            organization=organization,
            post=post,
            area=area,
            on_behalf_of=on_behalf_of
        )
        self.assertEqual(membership.on_behalf_of_id, "e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec")

    def test_create_membership_contacts(self):
        membership = Membership.objects.language("en").get(id="0a44195b-c3c9-4040-8dbf-be1aa250b700")

        ContactDetail.objects.language("en").create(
            type="facebook.com",
            value="http://facebook.com/scaly_wag",
            content_object=membership
        )
        contact = membership.contact_details.language("en").get(type="facebook.com")
        self.assertEqual(contact.value, "http://facebook.com/scaly_wag")

    def test_create_membership_links(self):
        membership = Membership.objects.language("en").get(id="0a44195b-c3c9-4040-8dbf-be1aa250b700")
        Link.objects.language("en").create(
            url="http://facebook.com/scaly_wag",
            content_object=membership
        )

        links = membership.links.language("en").get(url="http://facebook.com/scaly_wag")
        self.assertEqual(links.url, "http://facebook.com/scaly_wag")

    def test_create_bad_date_membership(self):
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        area = Area.objects.language("en").get(id="640c0f1d-2305-4d17-97fe-6aa59f079cc4")
        on_behalf_of = Organization.objects.language("en").get(id="e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec")
        with self.assertRaises(ValidationError):
            membership=Membership.objects.language("en").create(
                label="Test full membership",
                start_date="abcd",
                end_date="abcd",
                person=person,
                organization=organization,
                post=post,
                area=area,
                on_behalf_of=on_behalf_of
            )
