from rest_framework.test import APITestCase
from popit.signals.handlers import *
from popit.models import *
from rest_framework import status


class PostCitationAPITestCase(APITestCase):
    fixtures = ["api_request_test_data.yaml"]

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