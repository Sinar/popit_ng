__author__ = 'sweemeng'
from popit.serializers import ContactDetailSerializer
from popit.serializers.exceptions import ContentObjectNotAvailable
from popit.signals.handlers import *
from popit.models import *
from popit.tests.base_testcase import BasePopitTestCase


class PersonContactDetailsSerializerTestCase(BasePopitTestCase):

    def test_fetch_person_contact_details_list(self):
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        contact_details = person.contact_details.untranslated().all()
        serializers = ContactDetailSerializer(contact_details, language="en", many=True)
        self.assertEqual(len(serializers.data), 1)
        self.assertEqual(serializers.data[0]["value"], "0123421221")

    def test_fetch_person_contact_details(self):
        # a66cb422-eec3-4861-bae1-a64ae5dbde61
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')

        contact_details = person.contact_details.untranslated().get(id="a66cb422-eec3-4861-bae1-a64ae5dbde61")
        serializer = ContactDetailSerializer(contact_details, language="en")
        self.assertEqual(serializer.data["value"], "0123421221")

    def test_create_person_contact_details(self):
        data = {
            "type":"twitter",
            "value": "sinarproject",
        }
        person = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        serializer = ContactDetailSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save(content_object=person)
        person_ = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        contact_details = person_.contact_details.language('en').get(type="twitter")
        self.assertEqual(contact_details.value, "sinarproject")

    def test_create_person_contact_details_without_parent(self):
        data = {
            "type":"twitter",
            "value": "sinarproject",
        }

        serializer = ContactDetailSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        with self.assertRaises(ContentObjectNotAvailable):
            serializer.save()

    def test_update_persons_contact_details(self):
        data = {
            "id": "a66cb422-eec3-4861-bae1-a64ae5dbde61",
            "value": "0123421222",
        }

        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')

        contact_details = person.contact_details.untranslated().get(id="a66cb422-eec3-4861-bae1-a64ae5dbde61")
        serializer = ContactDetailSerializer(contact_details, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()

        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        contact_details = person_.contact_details.language('en').get(id="a66cb422-eec3-4861-bae1-a64ae5dbde61")
        self.assertEqual(contact_details.value, "0123421222")

    def test_create_persons_contact_details_translated(self):
        # Translatino does not exist yet
        data = {
            "label": "emel mengster"
        }
        person = Person.objects.language('en').get(id='c2a241a0d1fd4483b60af7dd219de22d')
        contact_details = person.contact_details.untranslated().get(id="2525224ad1d94ccfac0f1aa38bf3c2de")

        serializer = ContactDetailSerializer(contact_details, data=data, language="ms", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        contact_details = person.contact_details.language("ms").get(id="2525224ad1d94ccfac0f1aa38bf3c2de")
        self.assertEqual(contact_details.label, "emel mengster")

    def test_update_persons_contact_details_translated(self):
        data = {
            "label": "fon sweemeng"
        }

        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        # In production language existence is checked and translated version is passed into serializer if exist
        contact_details = person.contact_details.language("ms").get(id="a66cb422-eec3-4861-bae1-a64ae5dbde61")

        serializer = ContactDetailSerializer(contact_details, data=data, language="ms", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()

        contact_details = person.contact_details.language("ms").get(id="a66cb422-eec3-4861-bae1-a64ae5dbde61")
        self.assertEqual(contact_details.label, "fon sweemeng")


    def test_fetch_persons_contact_details_translated(self):
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        contact_details = person.contact_details.untranslated().get(id="a66cb422-eec3-4861-bae1-a64ae5dbde61")
        serializer = ContactDetailSerializer(contact_details, language="ms")
        data = serializer.data
        self.assertEqual(data["language_code"], "ms")


class PersonContactDetailsNestedSerializerTestCase(BasePopitTestCase):

    def test_fetch_person_contact_details_nested(self):
        person = Person.objects.untranslated().get(id='ab1a5788e5bae955c048748fa6af0e97')
        serializer = PersonSerializer(person, language="en")
        data = serializer.data
        self.assertEqual(data["contact_details"][0]["id"], "a66cb422-eec3-4861-bae1-a64ae5dbde61")

    def test_fetch_person_contact_details_nested_translated(self):
        person = Person.objects.untranslated().get(id='ab1a5788e5bae955c048748fa6af0e97')
        serializer = PersonSerializer(person, language="ms")
        data = serializer.data
        self.assertEqual(data["contact_details"][0]["language_code"], "ms")

    def test_create_person_contact_details_nested(self):
        data = {
            "contact_details":[
                {
                    "type": "twitter",
                    "value": "sinarproject",
                }
            ]
        }
        person = Person.objects.untranslated().get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        serializer = PersonSerializer(person, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        contact_details = person.contact_details.language("en").get(type="twitter")
        self.assertEqual(contact_details.value, "sinarproject")


    def test_create_person_contact_details_nested_translated(self):
        data = {
            "contact_details": [
                {
                    "id":"2525224ad1d94ccfac0f1aa38bf3c2de",
                    "label": "emel mengster"
                }
            ]
        }
        person = Person.objects.untranslated().get(id='c2a241a0d1fd4483b60af7dd219de22d')
        serializer = PersonSerializer(person, data=data, language="ms", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        contact_details = person.contact_details.language("ms").get(id="2525224ad1d94ccfac0f1aa38bf3c2de")
        self.assertEqual(contact_details.label, "emel mengster")

    def test_update_person_contact_details_nested(self):
        pass

    def test_update_person_contact_details_translated(self):
        pass