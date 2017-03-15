__author__ = 'sweemeng'
from popit.signals.handlers import *
from popit.models import *
from popit.tests.base_testcase import BasePopitTestCase
from popit.serializers.minimized import MinPostSerializer


class PostSerializerTestCase(BasePopitTestCase):

    def test_fetch_post_serializer(self):
        post = Post.objects.untranslated().get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        serializer = PostSerializer(post, language="en")
        self.assertEqual(serializer.data["role"], "member")

    def test_create_post_minimal_field_serializer(self):
        data = {
            "role": "Honorary Member",
        }
        serializer = PostSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        post = Post.objects.language("en").get(role="Honorary Member")
        self.assertEqual(post.role, "Honorary Member")

    def test_create_post_serializer(self):
        data = {
            "label": "Honorary Member",
            "organization_id": "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3",
            "role": "Honorary Member",
            "area_id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
            "start_date": "2000-02-02",
            "end_date": "2030-02-02",
        }

        serializer = PostSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        post = Post.objects.language("en").get(role="Honorary Member")
        self.assertEqual(post.organization_id, "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")

    def test_update_post_serializer(self):
        data = {
            "label": "member"
        }
        post = Post.objects.untranslated().get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        serializer = PostSerializer(post, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        self.assertEqual(post.label, "member")

    def test_create_post_otherlabels_serializer(self):
        data = {
            "other_labels": [{
                "name": "sampan party"
            }]
        }
        post = Post.objects.untranslated().get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        serializer = PostSerializer(post, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        other_labels = post.other_labels.language("en").get(name="sampan party")
        self.assertEqual(other_labels.name, "sampan party")

    def test_update_post_otherlabels_serializer(self):
        data = {
            "other_labels": [
                {
                    "id":"aee39ddd-6785-4a36-9781-8e745c6359b7",
                    "name": "Bilge Rat"
                }
            ]
        }
        post = Post.objects.untranslated().get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        serializer = PostSerializer(post, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        other_labels = post.other_labels.language("en").get(id="aee39ddd-6785-4a36-9781-8e745c6359b7")
        self.assertEqual(other_labels.name, "Bilge Rat")

    def test_create_post_contacts_serializer(self):
        data = {
            "contact_details": [
                {
                    "type": "sms",
                    "value": "231313123131",
                }
            ]
        }
        post = Post.objects.untranslated().get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        serializer = PostSerializer(post, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        contact = post.contact_details.language("en").get(value="231313123131")
        self.assertEqual(contact.type, "sms")

    def test_update_post_contacts_serializer(self):
        data = {
            "contact_details": [
                {
                    "id": "7f3f67c4-6afd-4de9-880e-943560cf56c0",
                    "type": "phone"
                }
            ]
        }

        post = Post.objects.untranslated().get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        serializer = PostSerializer(post, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        contact = post.contact_details.language("en").get(id="7f3f67c4-6afd-4de9-880e-943560cf56c0")
        self.assertEqual(contact.type, "phone")

    def test_create_post_links_serializer(self):
        data = {
            "links": [
                {
                    "url": "http://www.yahoo.com"
                }
            ]
        }
        post = Post.objects.untranslated().get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        serializer = PostSerializer(post, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        link = post.links.language("en").get(url="http://www.yahoo.com")
        self.assertEqual(link.url, "http://www.yahoo.com")

    def test_update_post_links_serializer(self):
        data = {
            "links": [
                {
                    "id": "ce15a9ee-6742-4467-bbfb-c86459ee685b",
                    "note": "just a link"
                }
            ]
        }
        post = Post.objects.untranslated().get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        serializer = PostSerializer(post, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        link = post.links.language("en").get(id="ce15a9ee-6742-4467-bbfb-c86459ee685b")
        self.assertEqual(link.note, "just a link")

    def test_create_post_otherlabels_links(self):
        data = {
            "other_labels": [
                {
                    "id": "aee39ddd-6785-4a36-9781-8e745c6359b7",
                    "links": [
                        {
                            "url": "http://en.wikipedia.com"
                        }
                    ]
                }
            ]
        }

        post = Post.objects.untranslated().get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        serializer = PostSerializer(post, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()

        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        other_labels = post.other_labels.language("en").get(id="aee39ddd-6785-4a36-9781-8e745c6359b7")
        link = other_labels.links.language("en").get(url="http://en.wikipedia.com")
        self.assertEqual(link.url, "http://en.wikipedia.com")

    def test_update_post_otherlabels_links(self):
        data = {
            "other_labels": [
                {
                    "id": "aee39ddd-6785-4a36-9781-8e745c6359b7",
                    "links": [
                        {
                            "id": "6c928027-4813-4770-80a5-ba413a43efae",
                            "note": "It is on facebook but it is hard to see"
                        }
                    ]
                }
            ]
        }

        post = Post.objects.untranslated().get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        serializer = PostSerializer(post, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()

        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        other_labels = post.other_labels.language("en").get(id="aee39ddd-6785-4a36-9781-8e745c6359b7")
        link = other_labels.links.language("en").get(id="6c928027-4813-4770-80a5-ba413a43efae")
        self.assertEqual(link.note, "It is on facebook but it is hard to see")

    def test_create_post_contact_links(self):
        data = {
            "contact_details": [
                {
                    "id": "7f3f67c4-6afd-4de9-880e-943560cf56c0",
                    "links": [
                        {
                            "url": "http://www.bing.com"
                        }
                    ]
                }
            ]
        }
        post = Post.objects.untranslated().get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        serializer = PostSerializer(post, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()

        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        contact = post.contact_details.language("en").get(id="7f3f67c4-6afd-4de9-880e-943560cf56c0")
        link = contact.links.language("en").get(url="http://www.bing.com")
        self.assertEqual(link.url, "http://www.bing.com")

    def test_update_post_contact_links(self):
        data = {
            "contact_details": [
                {
                    "id": "7f3f67c4-6afd-4de9-880e-943560cf56c0",
                    "links": [
                        {
                            "id": "a37256e6-eab7-417a-8ac8-32edc5031924",
                            "note": "a wikipedia site"
                        }
                    ]
                }
            ]
        }
        post = Post.objects.untranslated().get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        serializer = PostSerializer(post, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()

        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        contact = post.contact_details.language("en").get(id="7f3f67c4-6afd-4de9-880e-943560cf56c0")
        link = contact.links.language("en").get(id="a37256e6-eab7-417a-8ac8-32edc5031924")
        self.assertEqual(link.note, "a wikipedia site")

    def test_serializer_create_post_invalid_date(self):
        data = {
            "label": "Honorary Member",
            "organization_id": "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3",
            "role": "Honorary Member",
            "area_id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
            "start_date": "invalid date",
            "end_date": "invalid date",
        }

        serializer = PostSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_create_post_serializer_invalid_organization(self):
        data = {
            "label": "Honorary Member",
            "organization_id": "not exist",
            "role": "Honorary Member",
            "area_id": "640c0f1d-2305-4d17-97fe-6aa59f079cc4",
            "start_date": "2000-02-02",
            "end_date": "2030-02-02",
        }

        serializer = PostSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_create_post_serializer_invalid_area_id(self):
        data = {
            "label": "Honorary Member",
            "organization_id": "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3",
            "role": "Honorary Member",
            "area_id": "not exist",
            "start_date": "2000-02-02",
            "end_date": "2030-02-02",
        }

        serializer = PostSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_create_post_translated(self):
        data = {
            "label": "Ahli Terhormat",
            "role": "Ahli Terhormat",
        }
        serializer = PostSerializer(data=data, language="ms")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        post = Post.objects.language("ms").get(role="Ahli Terhormat")
        self.assertEqual(post.role, "Ahli Terhormat")

    def test_update_post_translated(self):
        data = {
            "label": "ahli"
        }
        # When translation do not exist, the following is used in production
        # post = Post.objects.untranslated().get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        # But when translation exist, fetch existing translation
        post = Post.objects.language("ms").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        serializer = PostSerializer(post, data=data, language="ms", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        post = Post.objects.language("ms").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        self.assertEqual(post.label, "ahli")

    def test_fetch_post_membership_translated(self):
        post = Post.objects.untranslated().get(id="2c6982c2-504a-4e0d-8949-dade5f9e494e")
        serializer = PostSerializer(post, language="ms")
        data = serializer.data
        for membership in data["memberships"]:
            self.assertEqual(membership["language_code"], "ms")

    def test_fetch_post_membership_organization_translated(self):
        post = Post.objects.untranslated().get(id="2c6982c2-504a-4e0d-8949-dade5f9e494e")
        serializer = PostSerializer(post, language="ms")
        data = serializer.data
        for membership in data["memberships"]:
            if membership["organization"]:
                self.assertEqual(membership["organization"]["language_code"], "ms")

    def test_fetch_post_membership_person_translated(self):
        post = Post.objects.untranslated().get(id="2c6982c2-504a-4e0d-8949-dade5f9e494e")
        serializer = PostSerializer(post, language="ms")
        data = serializer.data
        for membership in data["memberships"]:
            self.assertEqual(membership["person"]["language_code"], "ms")

    def test_fetch_post_organization_translated(self):
        post = Post.objects.untranslated().get(id="2c6982c2-504a-4e0d-8949-dade5f9e494e")
        serializer = PostSerializer(post, language="ms")
        data = serializer.data
        self.assertEqual(data["organization"]["language_code"], "ms")

    def test_fetch_post_membership_on_behalf_of_expanded(self):
        post = Post.objects.untranslated().get(id="3eb967bb-23e3-41b6-8cba-54aadac8d918")
        serializer = PostSerializer(post, language="en")
        data = serializer.data
        membership = data["memberships"][0]
        self.assertEqual(membership["on_behalf_of"]["id"],"3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")

    def test_minify_post_serializer(self):
        post = Post.objects.untranslated().get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        post_serializer = MinPostSerializer(post)
        membership_count = post.memberships.count()
        serializer_memberships = post_serializer.data["memberships"]
        self.assertEqual(len(serializer_memberships), membership_count)

    def test_update_post_null_value(self):
        data = {
            "role": None
        }
        post = Post.objects.untranslated().get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        serializer = PostSerializer(post, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        self.assertEqual(post.role, None)


    def test_update_post_area_null(self):
        data = {
            "area_id": None
        }

        post = Post.objects.untranslated().get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        serializer = PostSerializer(post, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        self.assertEqual(post.area, None)


