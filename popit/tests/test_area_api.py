from rest_framework import status
from rest_framework.authtoken.models import Token
from popit.tests.base_testcase import BasePopitAPITestCase
from popit.models.misc import Area


class AreaAPITestCase(BasePopitAPITestCase):

    def test_create_area_api(self):
        data = {
            "name": "petaling jaya",
            "classification": "town"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        client = self.client.post("/en/areas/", data=data)
        self.assertEqual(client.status_code, status.HTTP_201_CREATED)

    def test_create_area_translated_api(self):
        data = {
            "name": "petaling jaya",
            "classification": "town"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        client = self.client.post("/ms/areas/", data=data)
        self.assertEqual(client.status_code, status.HTTP_201_CREATED)

    def test_fetch_area_serializer(self):
        client = self.client.get("/en/areas/b0c2dbaba8ea476f91db1e3c2320dcb7")
        self.assertEqual(client.status_code, status.HTTP_200_OK)

    def test_update_area_api(self):
        data = {
            "identifier": "P21"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        client = self.client.put("/en/areas/b0c2dbaba8ea476f91db1e3c2320dcb7", data=data)
        self.assertEqual(client.status_code, status.HTTP_200_OK)

    def test_update_area_translated_api(self):
        data = {
            "name": "Subang Jaya",
            "classification": "bandar"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        client = self.client.put("/ms/areas/b0c2dbaba8ea476f91db1e3c2320dcb7", data=data)
        self.assertEqual(client.status_code, status.HTTP_200_OK)

        area = Area.objects.language("ms").get(id="b0c2dbaba8ea476f91db1e3c2320dcb7")
        self.assertEqual(area.classification, "bandar")

        area = Area.objects.language("en").get(id="b0c2dbaba8ea476f91db1e3c2320dcb7")
        self.assertNotEqual(area.classification, "bandar")

    def test_update_area_name_translated_api(self):
        data = {
            "name": "Bandar Subang Jaya",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        client = self.client.put("/ms/areas/b0c2dbaba8ea476f91db1e3c2320dcb7", data=data)
        self.assertEqual(client.status_code, status.HTTP_200_OK)

        area = Area.objects.language("ms").get(id="b0c2dbaba8ea476f91db1e3c2320dcb7")
        self.assertEqual(area.name, "Bandar Subang Jaya")

        area = Area.objects.language("en").get(id="b0c2dbaba8ea476f91db1e3c2320dcb7")
        self.assertNotEqual(area.name, "Bandar Subang Jaya")

