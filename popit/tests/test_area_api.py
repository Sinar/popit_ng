from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from popit.models import *


class AreaAPITestCase(APITestCase):
    fixtures = [ "api_request_test_data.yaml" ]

    def test_create_area_serializer(self):
        pass

    def test_fetch_area_serializer(self):
        client = self.client.get("/en/areas/b0c2dbaba8ea476f91db1e3c2320dcb7")
        

    def test_update_area_serializer(self):
        pass