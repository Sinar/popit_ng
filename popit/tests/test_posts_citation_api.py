from rest_framework.test import APITestCase
from popit.signals.handlers import *
from popit.models import *
from rest_framework import status


class PostCitationAPITestCase(APITestCase):
    fixtures = ["api_request_test_data.yaml"]

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

    def test_fetch_post_field_citation(self):
        response = self.client.get(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/citations/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_post_citation_list(self):
        response = self.client.get(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/citations/label/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_post_citation_detail(self):
        response = self.client.get(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/citations/label/cd23fabe24b1463ea971b9516717cedb/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_citation_unauthorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }

        response = self.client.post(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/citations/label/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_citation_authorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/citations/label/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        citations = post.links.filter(field="label")
        self.assertEqual(citations.count(), 2)

    def test_update_post_citation_unauthorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }

        response = self.client.put(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/citations/label/cd23fabe24b1463ea971b9516717cedb/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_citation_authorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/citations/label/cd23fabe24b1463ea971b9516717cedb/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post_citation_unauthorized(self):
        response = self.client.delete("/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/citations/label/cd23fabe24b1463ea971b9516717cedb/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_citation_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/citations/label/cd23fabe24b1463ea971b9516717cedb/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PostOtherLabelsCitationAPITestCase(APITestCase):
    fixtures = ["api_request_test_data.yaml"]

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

    def test_fetch_post_otherlabels_field_citations(self):
        response = self.client.get(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/aee39ddd-6785-4a36-9781-8e745c6359b7/citations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_post_otherlabels_citations_list(self):
        response = self.client.get(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/aee39ddd-6785-4a36-9781-8e745c6359b7/citations/name/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_post_otherlabels_citations_detail(self):
        response = self.client.get(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/aee39ddd-6785-4a36-9781-8e745c6359b7/citations/name/2640751d84034290812bc2eca880a3cf/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_otherlabels_citation_unauthorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }
        response = self.client.post(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/aee39ddd-6785-4a36-9781-8e745c6359b7/citations/name/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_otherlabels_citation_authorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/aee39ddd-6785-4a36-9781-8e745c6359b7/citations/name/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        otherlabels = post.other_labels.get(id="aee39ddd-6785-4a36-9781-8e745c6359b7")
        citations = otherlabels.links.filter(field="name")
        self.assertEqual(citations.count(),2)

    def test_update_post_otherlabels_citation_unauthorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }

        response = self.client.put(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/aee39ddd-6785-4a36-9781-8e745c6359b7/citations/name/2640751d84034290812bc2eca880a3cf/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_otherlabels_citation_authorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/aee39ddd-6785-4a36-9781-8e745c6359b7/citations/name/2640751d84034290812bc2eca880a3cf/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post_otherlabels_citations_unauthorized(self):
        response = self.client.delete(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/aee39ddd-6785-4a36-9781-8e745c6359b7/citations/name/2640751d84034290812bc2eca880a3cf/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_otherlabels_citations_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.delete(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/other_labels/aee39ddd-6785-4a36-9781-8e745c6359b7/citations/name/2640751d84034290812bc2eca880a3cf/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PostContactDetailCitationAPITestCase(APITestCase):
    fixtures = ["api_request_test_data.yaml"]

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

    def test_fetch_posts_contactdetails_field_citations(self):
        response = self.client.get(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/7f3f67c4-6afd-4de9-880e-943560cf56c0/citations"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_post_contactdetails_citation_detail(self):
        response = self.client.get(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/7f3f67c4-6afd-4de9-880e-943560cf56c0/citations/label/66e803c197f84587b5510232599ae536"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/7f3f67c4-6afd-4de9-880e-943560cf56c0/citations/label"
        )
        def test_fetch_posts_contactdetails_citations_list(self):
            self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_post_contactdetails_citation_unauthorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }
        response = self.client.post(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/7f3f67c4-6afd-4de9-880e-943560cf56c0/citations/label",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_contactdetails_citation_authorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/7f3f67c4-6afd-4de9-880e-943560cf56c0/citations/label",
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")
        contact_detail = post.contact_details.get(id="7f3f67c4-6afd-4de9-880e-943560cf56c0")
        citations = contact_detail.links.filter(field="label")
        self.assertEqual(citations.count(), 2)

    def test_update_post_contactdetailks_citation_unauthorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }

        response = self.client.put(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/7f3f67c4-6afd-4de9-880e-943560cf56c0/citations/label/66e803c197f84587b5510232599ae536",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_post_contactdetails_citation_authorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/7f3f67c4-6afd-4de9-880e-943560cf56c0/citations/label/66e803c197f84587b5510232599ae536",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_post_contactdetails_citation_unauthorized(self):
        response = self.client.delete(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/7f3f67c4-6afd-4de9-880e-943560cf56c0/citations/label/66e803c197f84587b5510232599ae536"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_post_contactdetails_citation_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/posts/c1f0f86b-a491-4986-b48d-861b58a3ef6e/contact_details/7f3f67c4-6afd-4de9-880e-943560cf56c0/citations/label/66e803c197f84587b5510232599ae536"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)