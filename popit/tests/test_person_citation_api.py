from popit.signals.handlers import *
from popit.models import *
from rest_framework import status
from popit.tests.base_testcase import BasePopitAPITestCase


class PersonCitationAPITestCase(BasePopitAPITestCase):

    def test_fetch_person_field_citation(self):
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/citations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        person = Person.objects.language("en").get(id="ab1a5788e5bae955c048748fa6af0e97")
        for field in person._meta.fields:
            if field.attname == "id":
                continue
            self.assertTrue(field.attname in data["result"])
        for field in person._translated_field_names:
            if field == "master_id" or field == "id":
                continue
            self.assertTrue(field in data["result"])

    def test_fetch_person_citation_list(self):
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/citations/email/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(len(data["results"]), 1)

    def test_fetch_person_citation_not_exists(self):
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/citations/email/not_exists/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_fetch_person_citation_exists(self):
        response = self.client.get("/en/persons/ab1a5788e5bae955c048748fa6af0e97/citations/email/7e462cdea35840a28c20cf9fe79284fd/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data["result"]["url"], "http://sinarproject.org")

    def test_add_person_citation_unauthorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }

        response = self.client.post("/en/persons/ab1a5788e5bae955c048748fa6af0e97/citations/name/", data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_person_citation_authorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post("/en/persons/ab1a5788e5bae955c048748fa6af0e97/citations/name/", data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        person = Person.objects.language("en").get(id="ab1a5788e5bae955c048748fa6af0e97")
        citations = person.links.filter(field="name")
        self.assertEqual(citations.count(), 2)

    def test_update_person_citation_unauthorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/citations/email/7e462cdea35840a28c20cf9fe79284fd/"
                                   , data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_api_authorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/citations/email/7e462cdea35840a28c20cf9fe79284fd/"
            , data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestPersonContactDetailCitationAPI(BasePopitAPITestCase):

    def test_fetch_person_contact_details_field_citations(self):
        response = self.client.get(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/citations"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_person_contact_details_citation_list(self):
        response = self.client.get(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/citations/label/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_person_contact_details_citation_detail(self):
        response = self.client.get(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/citations/label/10c5968966c84f6dacdd9ddd2613dc54/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_person_contact_details_citation_unauthorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }
        response = self.client.post("/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/citations/label/",
                                    data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_person_contact_details_citation_authorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/citations/label/",
            data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        person = Person.objects.language("en").get(id="ab1a5788e5bae955c048748fa6af0e97")
        contact_details = person.contact_details.get(id="a66cb422-eec3-4861-bae1-a64ae5dbde61")
        citations = contact_details.links.filter(field="label")
        self.assertEqual(citations.count(), 3)

    def test_update_person_contact_details_citation_unauthorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }
        response = self.client.put("/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/citations/label/10c5968966c84f6dacdd9ddd2613dc54/",
                                   data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_contact_details_citation_authorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.put(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/citations/label/10c5968966c84f6dacdd9ddd2613dc54/",
            data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_person_contact_details_citations_unauthorized(self):
        response = self.client.delete("/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/citations/label/10c5968966c84f6dacdd9ddd2613dc54/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_contact_details_citations_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/persons/ab1a5788e5bae955c048748fa6af0e97/contact_details/a66cb422-eec3-4861-bae1-a64ae5dbde61/citations/label/10c5968966c84f6dacdd9ddd2613dc54/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PersonOtherNameCitationsAPI(BasePopitAPITestCase):

    def test_fetch_person_other_name_field_citation(self):
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/citations"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_person_other_name_citation_list(self):
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/citations/name/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_person_other_name_citation_detail(self):
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/citations/name/83830211ee1642c79cfb5ad9df3c4169"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_person_other_name_citation_unauhtorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }
        response = self.client.post("/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/citations/name/",
                                    data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_person_other_name_citation_auhtorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

        response = self.client.post(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/citations/name/",
            data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        othername = person.other_names.get(id="cf93e73f-91b6-4fad-bf76-0782c80297a8")
        citations = othername.links.filter(field="name")
        # TODO: This is horrible, find better way to check the amount
        self.assertEqual(citations.count(), 4)

    def test_update_person_othername_citation_unauthorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }

        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/citations/name/83830211ee1642c79cfb5ad9df3c4169",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_othername_citation_authorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/citations/name/83830211ee1642c79cfb5ad9df3c4169",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_person_othername_unauthorized(self):
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/citations/name/83830211ee1642c79cfb5ad9df3c4169"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_othername_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/othernames/cf93e73f-91b6-4fad-bf76-0782c80297a8/citations/name/83830211ee1642c79cfb5ad9df3c4169"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class PersonIdentifierAPITestCase(BasePopitAPITestCase):

    def test_fetch_person_identifier_field_citation(self):
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/citations/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_person_identifier_citation_list(self):
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/citations/identifier/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fetch_person_identifier_citation_detail(self):
        response = self.client.get(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/citations/identifier/54e67687d6364c86a4a9adbd24d443ee/"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_add_person_identifier_citation_unauthorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }
        response = self.client.post(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/citations/identifier/",
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_person_idenfifier_citation_authorized(self):
        data = {
            "url": "http://twitter.com/sinarproject",
            "note": "just the twitter page"
        }

        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.post(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/citations/identifier/",
            data=data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        identifier = person.identifiers.get(id="34b59cb9-607a-43c7-9d13-dfe258790ebf")
        citations = identifier.links.filter(field="identifier")
        self.assertEqual(citations.count(), 2)

    def test_update_person_identifier_citation_unauthorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }

        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/citations/identifier/54e67687d6364c86a4a9adbd24d443ee/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_person_identifier_citation_authorized(self):
        data = {
            "url": "http://www.sinarproject.org"
        }
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.put(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/citations/identifier/54e67687d6364c86a4a9adbd24d443ee/",
            data=data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_person_identifier_citation_unauthorized(self):
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/citations/identifier/54e67687d6364c86a4a9adbd24d443ee/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_person_identifier_citation_authorized(self):
        token = Token.objects.get(user__username="admin")
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        response = self.client.delete(
            "/en/persons/8497ba86-7485-42d2-9596-2ab14520f1f4/identifiers/34b59cb9-607a-43c7-9d13-dfe258790ebf/citations/identifier/54e67687d6364c86a4a9adbd24d443ee/"
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
