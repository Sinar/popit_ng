from rest_framework.test import APITestCase
from popit.models import Person
from popit.models import Identifier
from popit.signals.handlers import *
from rest_framework import status


class PersonIdentifierIndividualAPITestCase(APITestCase):
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

    def test_fetch_person_identifier(self):
        response = self.client.get("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["result"]["identifier"], "53110321")

    def test_fetch_person_identifier_translated(self):
        response = self.client.get(
            "/ms/persons/ab1a5788e5bae955c048748fa6af0e97/identifiers/94318759d80c4533bcca0971bc516500/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["result"]["identifier"], "123342343242")

    def test_create_person_identifier_authorized(self):
        data = {
            "identifier": "123121231",
            "scheme": "test_identifier"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/persons/078541c9-9081-4082-b28f-29cbb64440cb/identifiers/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        person = Person.objects.language("en").get(id="078541c9-9081-4082-b28f-29cbb64440cb")
        identifiers = person.identifiers.language("en").get(identifier="123121231")
        self.assertEqual(identifiers.scheme, "test_identifier")

    def test_create_person_identifier_unauthorized(self):
        data = {
            "identifier": "123121231",
            "scheme": "test_identifier"
        }

        response = self.client.post("/en/persons/078541c9-9081-4082-b28f-29cbb64440cb/identifiers/", data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_person_identifier_translated_authorized(self):
        data = {
            "identifier": "123121231",
            "scheme": "id_percubaan"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/ms/persons/078541c9-9081-4082-b28f-29cbb64440cb/identifiers/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        person = Person.objects.untranslated().get(id="078541c9-9081-4082-b28f-29cbb64440cb")
        identifier = person.identifiers.language("ms").get(identifier="123121231")
        self.assertEqual(identifier.scheme, "id_percubaan")

    def test_update_person_identifier_translated_authorized(self):
        data = {
            "scheme": "Kad Pengenalan"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/ms/persons/ab1a5788e5bae955c048748fa6af0e97/identifiers/94318759d80c4533bcca0971bc516500", data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person = Person.objects.untranslated().get(id="ab1a5788e5bae955c048748fa6af0e97")
        identifier = person.identifiers.language("ms").get(id="94318759d80c4533bcca0971bc516500")
        self.assertEqual(identifier.scheme, "Kad Pengenalan")

    def test_view_person_identifier_list_unauthorized(self):
        response = self.client.get("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_person_identifier_list_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_view_person_identifier_detail_unauthorized(self):
        response = self.client.get("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"]["identifier"], "53110321")

    def test_view_person_identifier_detail_not_exist_unauthorized(self):
        response = self.client.get("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/not_exist/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_person_identifier_detail_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["result"]["identifier"], "53110321")

    def test_view_person_identifier_detail_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_person_identifier_unauthorized(self):
        data = {
            "identifier": "53110322",
        }
        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_identifier_not_exist_unauthorized(self):
        data = {
            "identifier": "53110322",
        }
        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/not_exist/",
            data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_identifier_authorized(self):
        data = {
            "identifier": "53110322",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/",
            data
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        person_ = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        identifier = person_.identifiers.language('en').get(id="34b59cb9-607a-43c7-9d13-dfe258790ebf")
        self.assertEqual(identifier.identifier, '53110322')

    def test_update_person_identifier_not_exist_authorized(self):
        data = {
            "identifier": "53110322",
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/not_exist/",
            data
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_person_identifier_unauthorized(self):
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_identifer_not_exist_unauthorized(self):
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_identifier_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_person_identifier_not_exist_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/not_exist/"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



class PersonIdentifierNestedAPITestCase(APITestCase):
    fixtures = [ "api_request_test_data.yaml" ]

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

    def test_create_person_identifier_unauthorized(self):
        person_data = {
            "identifiers": [
                {
                    "scheme": "IC",
                    "identifier": "129031309",
                }
            ]
        }
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/", person_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_person_identifier_authorized(self):
        person_data = {
            "identifiers": [
                {
                    "scheme": "IC",
                    "identifier": "129031309",
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/", person_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')

        identifier = person_.identifiers.language('en').get(identifier="129031309")
        self.assertEqual(identifier.scheme, "IC")

    def test_update_person_identifier_unauthorized(self):
        person_data = {
            "identifiers": [
                {
                    "id": "34b59cb9-607a-43c7-9d13-dfe258790ebf",
                    "identifier": "53110322",
                }
            ]
        }
        # 8497ba86-7485-42d2-9596-2ab14520f1f4
        response = self.client.put("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/", person_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_identifier_authorized(self):
        person_data = {
            "identifiers": [
                {
                    "id": "34b59cb9-607a-43c7-9d13-dfe258790ebf",
                    "identifier": "53110322",
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/", person_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person_ = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        identifier = person_.identifiers.language('en').get(id="34b59cb9-607a-43c7-9d13-dfe258790ebf")
        self.assertEqual(identifier.identifier, '53110322')

    def test_create_person_identifier_translated_authorized(self):
        data = {
            "identifiers": [
                {
                    "identifier": "123121231",
                    "scheme": "id_percubaan"
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/ms/persons/078541c9-9081-4082-b28f-29cbb64440cb/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person = Person.objects.untranslated().get(id="078541c9-9081-4082-b28f-29cbb64440cb")
        identifier = person.identifiers.language("ms").get(identifier="123121231")
        self.assertEqual(identifier.scheme, "id_percubaan")

    def test_update_person_identifier_translated_authorized(self):
        data = {
            "identifiers": [
                {
                    "id": "94318759d80c4533bcca0971bc516500",
                    "scheme": "Kad Pengenalan"
                }
            ]
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put("/ms/persons/ab1a5788e5bae955c048748fa6af0e97/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        person = Person.objects.untranslated().get(id="ab1a5788e5bae955c048748fa6af0e97")
        identifier = person.identifiers.language("ms").get(id="94318759d80c4533bcca0971bc516500")
        self.assertEqual(identifier.scheme, "Kad Pengenalan")
