from popit.signals.handlers import *
from popit.models import *
from rest_framework import status
from popit.tests.base_testcase import BasePopitAPITestCase


class PostCitationAPITestCase(BasePopitAPITestCase):

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


class PostOtherLabelsCitationAPITestCase(BasePopitAPITestCase):

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


class PostContactDetailCitationAPITestCase(BasePopitAPITestCase):

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