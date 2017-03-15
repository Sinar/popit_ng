from rest_framework import status
from popit.signals.handlers import *
import logging
from django.conf import settings
from popit.tests.base_testcase import BasePopitAPITestCase


class RelationAPITestCasse(BasePopitAPITestCase):

    def test_list_relation(self):
        response = self.client.get("/en/relations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("page" in response.data)
        self.assertEqual(response.data["per_page"], settings.REST_FRAMEWORK["PAGE_SIZE"])

    def test_fetch_relation_detail(self):
        response = self.client.get("/en/relations/0d41f7b50df743db95982a2b3c20e999/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_relation_detail_not_exist(self):
        response = self.client.get("/en/relations/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_relation_unauthorized(self):
        data = {
            "label": "test relation",
            "object_id":"078541c9-9081-4082-b28f-29cbb64440cb",
            "subject_id": "2439e472-10dc-4f9c-aa99-efddd9046b4a",
        }
        response = self.client.post("/en/relations/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_relation_authorized(self):
        data = {
            "label": "test relation",
            "object_id":"078541c9-9081-4082-b28f-29cbb64440cb",
            "subject_id": "2439e472-10dc-4f9c-aa99-efddd9046b4a",
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/relations/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_relation_without_subject_unauthorized(self):
        data = {
            "label": "test relation",
            "object_id":"078541c9-9081-4082-b28f-29cbb64440cb",
        }

        response = self.client.post("/en/relations/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_relation_without_subject_authorized(self):
        data = {
            "label": "test relation",
            "object_id":"078541c9-9081-4082-b28f-29cbb64440cb",
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/relations/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("errors" in response.data)

    def test_create_relation_without_object_unauthorized(self):
        data = {
            "label": "test relation",
            "subject_id":"078541c9-9081-4082-b28f-29cbb64440cb",
        }

        response = self.client.post("/en/relations/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_relation_without_object_authorized(self):
        data = {
            "label": "test relation",
            "subject_id":"078541c9-9081-4082-b28f-29cbb64440cb",
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/relations/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("errors" in response.data)

    def test_update_relation_unauthorized(self):
        data = {
            "label": "sweemeng land lubber"
        }

        response = self.client.put("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_relation_not_exist_unauthorized(self):
        data = {
            "label": "sweemeng land lubber"
        }

        response = self.client.put("/en/relations/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_relation_authorized(self):
        data = {
            "label": "sweemeng land lubber"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_relation_not_exist_authorized(self):
        data = {
            "label": "sweemeng land lubber"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/relations/not_exist/", data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_relation_link_unauthorized(self):
        data = {
            "links": [
                {
                    "url": "http://thecaptain.tumblr.com",
                    "label": "Captain's Tumblr"
                }
            ]
        }

        response = self.client.put("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_relation_link_authorized(self):
        data = {
            "links": [
                {
                    "url": "http://thecaptain.tumblr.com",
                    "label": "Captain's Tumblr"
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_relation_link_unauthorized(self):
        data = {
            "links": [
                {
                    "id": "239edef4-af68-4ffb-adce-96d17cbea79d",
                    "label": "Captain's page"
                }
            ]
        }
        response = self.client.put("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/", data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_relation_link_authorized(self):
        data = {
            "links": [
                {
                    "id": "239edef4-af68-4ffb-adce-96d17cbea79d",
                    "label": "Captain's page"
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_relation_unauthorized(self):
        response = self.client.delete("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_relation_not_exist_unauthorized(self):
        response = self.client.delete("/en/relations/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_relation_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_relation_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete("/en/relations/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fetch_relation_translated_nested(self):
        response = self.client.get("/ms/relations/732d7ea706024973aa364b0ffa9dc2a1/")
        results = response.data["result"]

        self.assertEqual(results["subject"]["name"], "jolly a/l roger")
        self.assertEqual(results["subject"]["language_code"], "ms")

    def test_fetch_relation_translated(self):
        response = self.client.get("/ms/relations/732d7ea706024973aa364b0ffa9dc2a1/")
        results = response.data["result"]
        self.assertEqual(results["label"], "Kawan Lanun")
        self.assertEqual(results["language_code"], "ms")

    def test_create_relation_invalid_date(self):
        data = {
            "label": "test relation",
            "object_id":"078541c9-9081-4082-b28f-29cbb64440cb",
            "subject_id": "2439e472-10dc-4f9c-aa99-efddd9046b4a",
            "start_date": "invalid date",
            "end_date": "invalid date"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/relations/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("errors" in response.data)

    def test_create_relation_valid_date(self):
        data = {
            "label": "test relation",
            "object_id":"078541c9-9081-4082-b28f-29cbb64440cb",
            "subject_id": "2439e472-10dc-4f9c-aa99-efddd9046b4a",
            "start_date": "2010-01-01",
            "end_date": "2015-01-01"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/relations/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_relation_invalid_object(self):
        data = {
            "label": "test relation",
            "object_id":"not_exist",
            "subject_id": "2439e472-10dc-4f9c-aa99-efddd9046b4a",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/relations/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue("errors" in response.data)

    def test_create_relation_invalid_subject(self):
        data = {
            "label": "test relation",
            "object_id":"078541c9-9081-4082-b28f-29cbb64440cb",
            "subject_id": "not_exist",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/en/relations/", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_relation_authorized_translated(self):
        data = {
            "label": "sweemeng adalah land lubber"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/ms/relations/732d7ea706024973aa364b0ffa9dc2a1/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"]["label"], "sweemeng adalah land lubber")

    def test_create_relation_with_translation(self):
        data = {
            "label": "percubaan relation",
            "object_id":"078541c9-9081-4082-b28f-29cbb64440cb",
            "subject_id": "2439e472-10dc-4f9c-aa99-efddd9046b4a",
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post("/ms/relations/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["result"]["label"], "percubaan relation")

    def test_create_relation_with_post_blank_id_authorized(self):
        data = {
            "id": "",
            "label": "test relation",
            "object_id":"078541c9-9081-4082-b28f-29cbb64440cb",
            "subject_id": "2439e472-10dc-4f9c-aa99-efddd9046b4a",
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/relations/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_relation_link_blank_id_authorized(self):
        data = {
            "links": [
                {
                    "id": "",
                    "url": "http://thecaptain.tumblr.com",
                    "label": "Captain's Tumblr"
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/relations/732d7ea706024973aa364b0ffa9dc2a1/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
