from rest_framework import status
from popit.signals.handlers import *
from popit.tests.base_testcase import BasePopitAPITestCase

class RelationLinkAPITestCase(BasePopitAPITestCase):

    def test_list_relation_link_api(self):
        response = self.client.get("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/links/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_relation_link_detail_api(self):
        response = self.client.get("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/links/31812ed9d2fa405882f6f300a7f8c843/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_relation_link_detail_api_not_exist(self):
        response = self.client.get("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_relation_link_api_unauthorized(self):
        data = {
            "url": "http://thecaptain.tumblr.com",
            "label": "Captain's Tumblr"
        }
        response = self.client.post("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/links/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_relation_link_api_authorized(self):
        data = {
            "url": "http://thecaptain.tumblr.com",
            "label": "Captain's Tumblr"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/links/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_relation_link_api_not_exist_unauthorized(self):
        data = {
            "id": "239edef4-af68-4ffb-adce-96d17cbea79d",
            "label": "Captain's page"
        }
        response = self.client.put("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/links/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_relation_link_api_not_exist_authorized(self):
        data = {
            "id": "239edef4-af68-4ffb-adce-96d17cbea79d",
            "label": "Captain's page"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/links/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_relation_link_api_exist_unauthorized(self):
        data = {
            "id": "239edef4-af68-4ffb-adce-96d17cbea79d",
            "label": "Captain's page"
        }
        response = self.client.put("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/links/31812ed9d2fa405882f6f300a7f8c843/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_relation_link_api_exist_authorized(self):
        data = {
            "id": "239edef4-af68-4ffb-adce-96d17cbea79d",
            "label": "Captain's page"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/links/31812ed9d2fa405882f6f300a7f8c843/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_relation_link_api_not_exist_unauthorized(self):
        response = self.client.delete("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_relation_link_api_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/links/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_relation_link_api_exist_unauthorized(self):
        response = self.client.delete("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/links/31812ed9d2fa405882f6f300a7f8c843/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_relation_link_api_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/links/31812ed9d2fa405882f6f300a7f8c843/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class RelationIdentifierAPITestCase(BasePopitAPITestCase):

    def test_list_relation_identifier(self):
        response = self.client.get("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/identifiers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_show_relation_identifier_not_exist(self):
        response = self.client.get("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/identifiers/not_exists/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_show_relation_identifier(self):
        response = self.client.get("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/identifiers/ea7a6f409d6d4352ab02b0a099792653/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_relation_identifier_unauthorized(self):
        data = {
            "scheme": "testing",
            "identifier": "12319021390"
        }
        response = self.client.post("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/identifiers/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_relation_identifier_authorized(self):
        data = {
            "scheme": "testing",
            "identifier": "12319021390"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/identifiers/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        relation = Relation.objects.language("en").get(id="732d7ea706024973aa364b0ffa9dc2a1")
        identifier = relation.identifiers.language("en").get(identifier="12319021390")
        self.assertEqual(identifier.scheme, "testing")

    def test_update_relation_identifier_not_exist_unauthorized(self):
        data = {
            "identifier": "3131313"
        }
        response = self.client.put(
            "/en/relations/732d7ea706024973aa364b0ffa9dc2a1/identifiers/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_relation_identifier_not_exist_authorized(self):
        data = {
            "identifier": "3131313"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/relations/732d7ea706024973aa364b0ffa9dc2a1/identifiers/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_relation_identifier_unauthorized(self):
        data = {
            "identifier": "3131313"
        }
        response = self.client.put(
            "/en/relations/732d7ea706024973aa364b0ffa9dc2a1/identifiers/ea7a6f409d6d4352ab02b0a099792653/",
            data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_relation_identifier_authorized(self):
        data = {
            "identifier": "3131313"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/relations/732d7ea706024973aa364b0ffa9dc2a1/identifiers/ea7a6f409d6d4352ab02b0a099792653/",
            data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_relation_identifier_not_exist_unauthorized(self):
        response = self.client.delete("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/identifiers/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_relation_identifier_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/identifiers/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_relation_identifier_unauthorized(self):
        response = self.client.delete("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/identifiers/ea7a6f409d6d4352ab02b0a099792653/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_relation_identifier_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/identifiers/ea7a6f409d6d4352ab02b0a099792653/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
