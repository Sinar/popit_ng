__author__ = 'sweemeng'
from rest_framework import status
from popit.signals.handlers import *
from popit.models import *
from popit.tests.base_testcase import BasePopitAPITestCase

class PersonContactAPITestCase(BasePopitAPITestCase):

    def test_view_person_contact_list_unauthorized(self):
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["value"], "0123421221")

    def test_view_person_contact_list_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["value"], "0123421221")

    def test_view_person_contact_detail_unauthorized(self):
        response = self.client.get(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"]["value"], "0123421221")

    def test_view_person_contact_detail_not_exist_unauthorized(self):
        response = self.client.get(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_person_contact_detail_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"]["value"], "0123421221")

    def test_view_person_contact_detail_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_person_contact_unauthorized(self):
        data = {
            "type":"twitter",
            "value": "sinarproject",
        }

        request = self.client.post(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/contact_details/",
            data
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_person_contact_authorized(self):
        data = {
            "type":"twitter",
            "value": "sinarproject",
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        request = self.client.post(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/contact_details/",
            data
        )
        self.assertEqual(request.status_code, status.HTTP_201_CREATED)
        person_ = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        contact = person_.contact_details.language('en').get(type="twitter")
        self.assertEqual(contact.value, "sinarproject")

    def test_update_person_contact_unauthorized(self):
        data = {

            "value": "0123421222",
        }

        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        request = self.client.put(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/",
            data
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_contact_not_exist_unauthorized(self):
        data = {

            "value": "0123421222",
        }

        request = self.client.put(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/not_exist/",
            data
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_contact_authorized(self):
        data = {

            "value": "0123421222",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        request = self.client.put(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/",
            data
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        contact = person.contact_details.language('en').get(id="a66cb422-eec3-4861-bae1-a64ae5dbde61")
        self.assertEqual(contact.value, "0123421222")

    def test_update_person_contact_not_exist_authorized(self):
        data = {

            "value": "0123421222",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        request = self.client.put(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/not_exist/",
            data
        )
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_person_contact_unauthorized(self):
        request = self.client.delete(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/"
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_contact_not_exist_unauthorized(self):
        request = self.client.delete(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/not_exist/"
        )
        self.assertEqual(request.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_contact_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        request = self.client.delete(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/"
        )
        self.assertEqual(request.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_person_contact_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        request = self.client.delete(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/not_exist/"
        )
        self.assertEqual(request.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_person_contact_translated_authorized(self):
        data = {
            "label": "emel mengster"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        request = self.client.put(
            "/ms/persons/c2a241a0d1fd4483b60af7dd219de22d/contact_details/2525224ad1d94ccfac0f1aa38bf3c2de/",
            data
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        person = Person.objects.language('en').get(id='c2a241a0d1fd4483b60af7dd219de22d')
        contact_details = person.contact_details.language("ms").get(id="2525224ad1d94ccfac0f1aa38bf3c2de")
        self.assertEqual(contact_details.label, "emel mengster")


    def test_update_person_contact_translated_authorized(self):
        data = {
            "label": "fon sweemeng"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        request = self.client.put(
            "/ms/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/",
            data
        )
        self.assertEqual(request.status_code, status.HTTP_200_OK)
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        contact_details = person.contact_details.language("ms").get(id="a66cb422-eec3-4861-bae1-a64ae5dbde61")
        self.assertEqual(contact_details.label, "fon sweemeng")

    def test_fetch_person_contact_translated(self):
        request = self.client.get("/ms/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/")
        self.assertEqual(request.status_code, status.HTTP_200_OK)

        data = request.data
        self.assertEqual(data["result"]["language_code"], "ms")


class PersonContactNestedAPITestCase(BasePopitAPITestCase):

    def test_create_contact_unauthorized(self):
        person_data = {
            "contact_details": [
                {
                    "type":"twitter",
                    "value": "sinarproject",
                }
            ]
        }
        # 8497ba86-7485-42d2-9596-2ab14520f1f4
        response = self.client.put("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/", person_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_contact_authorized(self):
        person_data = {
            "contact_details": [
                {
                    "type":"twitter",
                    "value": "sinarproject",
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/", person_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        person_ = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        contact = person_.contact_details.language('en').get(type="twitter")
        self.assertEqual(contact.value, "sinarproject")

    def test_update_contact_unauthorized(self):
        person_data = {
            "contact_details": [
                {
                    "id": "a66cb422-eec3-4861-bae1-a64ae5dbde61",
                    "value": "0123421222",
                }
            ]
        }
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/", person_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_contact_authorized(self):
        person_data = {
            "contact_details": [
                {
                    "id": "a66cb422-eec3-4861-bae1-a64ae5dbde61",
                    "value": "0123421222",
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/", person_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        contact = person_.contact_details.language('en').get(id="a66cb422-eec3-4861-bae1-a64ae5dbde61")
        self.assertEqual(contact.value, "0123421222")