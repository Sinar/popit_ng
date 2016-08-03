from popit.serializers import IdentifierSerializer
from popit.serializers import PersonSerializer
from django.test import TestCase
from popit.signals.handlers import *
from popit.models import *


class PersonIdentifierTestCase(TestCase):
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

    def test_create_person_identifier(self):
        person = Person.objects.language("en").get(id="078541c9-9081-4082-b28f-29cbb64440cb")
        data = {
            "identifier": "123121231",
            "scheme":"test_identifier"
        }
        serializer = IdentifierSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save(content_object=person)
        identifiers = person.identifiers.language("en").get(identifier="123121231")
        self.assertEqual(identifiers.scheme, "test_identifier")

    def test_update_person_identifier(self):
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        identifier = Identifier.objects.language("en").get(id="34b59cb9-607a-43c7-9d13-dfe258790ebf")
        data = {
            "identifier":"531103213"
        }
        serializer = IdentifierSerializer(identifier, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        identifier = Identifier.objects.language("en").get(id="34b59cb9-607a-43c7-9d13-dfe258790ebf")
        self.assertEqual(identifier.identifier, "531103213")

    def test_fetch_person_identifier(self):
        identifier = Identifier.objects.language("en").get(id="34b59cb9-607a-43c7-9d13-dfe258790ebf")
        serializer = IdentifierSerializer(identifier, language="en")
        data = serializer.data
        self.assertEqual(data["identifier"], "53110321")

    def test_update_translation(self):
        identifier = Identifier.objects.untranslated().get(id="23b470bbc1884c378e447718e92c920b")
        serializer = IdentifierSerializer(identifier, language="ms")
        data = serializer.data
        self.assertEqual(data["language_code"], "ms")


class PersonNestedIdentifierTestCase(TestCase):
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

    def test_create_person_identifier_nested(self):
        person = Person.objects.language("en").get(id="078541c9-9081-4082-b28f-29cbb64440cb")
        data = {
            "identifiers":[
                {
                    "identifier": "123121231",
                    "scheme": "test_identifier"
                }
            ]
        }
        serializer = PersonSerializer(person, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        identifiers = person.identifiers.language("en").get(identifier="123121231")
        self.assertEqual(identifiers.scheme, "test_identifier")

    def test_update_person_identifier_nested(self):
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        data = {
            "identifiers": [
                {
                    "id": "34b59cb9-607a-43c7-9d13-dfe258790ebf",
                    "identifier": "531103213"
                }
            ]
        }
        serializer = PersonSerializer(person, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        identifier = Identifier.objects.language("en").get(id="34b59cb9-607a-43c7-9d13-dfe258790ebf")
        self.assertEqual(identifier.identifier, "531103213")

    def test_fetch_person_identifier_nested(self):
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        serializer = PersonSerializer(person, language="en")
        data = serializer.data

        identifiers = data["identifiers"]
        self.assertTrue(isinstance(identifiers, list))
        found = False
        for identifier in identifiers:
            if identifier["identifier"] == "53110321":
                found = True
                break
        self.assertTrue(found, "Item not found")

    def test_fetch_person_identifier_nested_translated(self):
        person = Person.objects.untranslated().get(id="ab1a5788e5bae955c048748fa6af0e97")
        serializer = PersonSerializer(person, language="ms")
        data = serializer.data
        identifiers = data["identifiers"]
        for identifier in identifiers:
            self.assertEqual(identifier["language_code"], "ms")

    def test_create_person_identifier_nested_translated(self):
        person = Person.objects.untranslated().get(id="078541c9-9081-4082-b28f-29cbb64440cb")
        data = {
            "identifiers": [
                {
                    "identifier": "123121231",
                    "scheme": "id_percubaan"
                }
            ]
        }
        serializer = PersonSerializer(person, data=data, language="ms", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        identifier = person.identifiers.language("ms").get(identifier="123121231")
        self.assertEqual(identifier.scheme, "id_percubaan")

    def test_update_person_identifier_nested_translated(self):
        data = {
            "identifiers": [
                {
                    "id": "94318759d80c4533bcca0971bc516500",
                    "scheme": "Kad Pengenalan"
                }
            ]
        }
        person = Person.objects.untranslated().get(id="ab1a5788e5bae955c048748fa6af0e97")
        serializer = PersonSerializer(person,data=data, language="ms", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        identifier = person.identifiers.language("ms").get(id="94318759d80c4533bcca0971bc516500")
        self.assertEqual(identifier.scheme, "Kad Pengenalan")