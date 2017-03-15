from popit.signals.handlers import *
from popit.models import *
from rest_framework import status
from popit.tests.base_testcase import BasePopitAPITestCase


class RelationCitationAPITestCase(BasePopitAPITestCase):

    def test_fetch_relation_field_citation(self):
        response = self.client.get(
            "/en/relations/732d7ea706024973aa364b0ffa9dc2a1/citations/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_relation_citation_list(self):
        response = self.client.get(
            "/en/relations/732d7ea706024973aa364b0ffa9dc2a1/citations/label"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_relation_citation_detail(self):
        response = self.client.get(
            "/en/relations/732d7ea706024973aa364b0ffa9dc2a1/citations/label/31812ed9d2fa405882f6f300a7f8c843"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_relation_citation_unauthorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }
        response = self.client.post(
            "/en/relations/732d7ea706024973aa364b0ffa9dc2a1/citations/label",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_relation_citation_authorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            "/en/relations/732d7ea706024973aa364b0ffa9dc2a1/citations/label",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        relation = Relation.objects.language("en").get(id="732d7ea706024973aa364b0ffa9dc2a1")

        citations = relation.links.filter(field="label")
        self.assertEqual(citations.count(), 2)

    def test_update_relation_citation_unauthorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }

        response = self.client.put(
            "/en/relations/732d7ea706024973aa364b0ffa9dc2a1/citations/label/31812ed9d2fa405882f6f300a7f8c843",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_relation_citation_authorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/relations/732d7ea706024973aa364b0ffa9dc2a1/citations/label/31812ed9d2fa405882f6f300a7f8c843",
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_relation_citation_unauthorized(self):
        response = self.client.delete("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/citations/label/31812ed9d2fa405882f6f300a7f8c843")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_relation_citation_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/citations/label/31812ed9d2fa405882f6f300a7f8c843")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


