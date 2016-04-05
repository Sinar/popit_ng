from rest_framework.test import APITestCase
from popit.signals.handlers import *
from popit.models import *
from rest_framework import status
import logging


class PersonCitationAPITestCase(APITestCase):
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


class TestPersonContactDetailCitationAPI(APITestCase):
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


class PersonOtherNameCitationsAPI(APITestCase):
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


class PersonIdentifierAPITestCase(APITestCase):
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
