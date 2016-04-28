__author__ = 'sweemeng'
from django.test import TestCase
from django.core.validators import ValidationError
from popit.models import Post
from popit.models import Organization
from popit.models import Area
from popit.models import OtherName
from popit.models import Link
from popit.models import ContactDetail
from popit.signals.handlers import *
from popit.models import *


class PostModelTestCase(TestCase):
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

    def test_create_post_minimum_field(self):
        post = Post.objects.language("en").create(
            role="director",
        )
        self.assertEqual(post.role, "director")

    def test_create_post(self):
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        area = Area.objects.language("en").get(id="640c0f1d-2305-4d17-97fe-6aa59f079cc4")
        post = Post.objects.language("en").create(
            label="leader",
            role="director",
            organization=organization,
            area=area,
            start_date="2000-02-02",
            end_date="2030-02-02",
        )
        self.assertEqual(post.label, "leader")

    def test_update_post(self):
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        post.label = "member"
        post.save()
        self.assertEqual(post.label, "member")

    def test_create_post_other_labels(self):
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        OtherName.objects.language("en").create(
            name="sampan party",
            content_object=post
        )
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        other_name = post.other_labels.language("en").get(name="sampan party")
        self.assertEqual(other_name.name, "sampan party")

    def test_update_post_other_labels(self):
        other_labels = OtherName.objects.language("en").get(id="aee39ddd-6785-4a36-9781-8e745c6359b7")
        other_labels.name = "Bilge Rat" # With capital B instead of not
        other_labels.save()

        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        other_labels = post.other_labels.language("en").get(id="aee39ddd-6785-4a36-9781-8e745c6359b7")
        self.assertEqual(other_labels.name, "Bilge Rat")

    def test_create_post_contacts(self):
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        ContactDetail.objects.language("en").create(
            value="231313123131",
            type="sms",
            content_object=post
        )
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        contact = post.contact_details.language("en").get(value="231313123131")
        self.assertEqual(contact.type, "sms")

    def test_update_post_contacts(self):
        contact = ContactDetail.objects.language("en").get(id="7f3f67c4-6afd-4de9-880e-943560cf56c0")
        contact.type="phone"
        contact.save()
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        contact = post.contact_details.language("en").get(id="7f3f67c4-6afd-4de9-880e-943560cf56c0")
        self.assertEqual(contact.type, "phone")

    def test_create_post_links(self):
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        link = Link.objects.language("en").create(
            url="http://www.yahoo.com",
            content_object=post
        )
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        link = post.links.language("en").get(url="http://www.yahoo.com")
        self.assertEqual(link.url, "http://www.yahoo.com")

    def test_update_post_links(self):
        link = Link.objects.language("en").get(id="ce15a9ee-6742-4467-bbfb-c86459ee685b")
        link.note = "just a link"
        link.save()
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        link = post.links.language("en").get(id="ce15a9ee-6742-4467-bbfb-c86459ee685b")
        self.assertEqual(link.note, "just a link")

    def test_create_post_citation(self):
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        post.add_citation("label", "http://google.com", "Just a note for test_case")

        link = post.links.language("en").filter(field="label", note="Just a note for test_case")
        self.assertEqual(link[0].url, "http://google.com")

    def test_create_post_invalid_date(self):
        with self.assertRaises(ValidationError):
            organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
            area = Area.objects.language("en").get(id="640c0f1d-2305-4d17-97fe-6aa59f079cc4")
            post = Post.objects.language("en").create(
                label="leader",
                role="director",
                organization=organization,
                area=area,
                start_date="bad",
                end_date="date",
            )

