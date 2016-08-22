__author__ = 'sweemeng'
from popit.serializers import LinkSerializer
from popit.serializers import OtherNameSerializer
from popit.serializers import AreaSerializer
from popit.serializers.exceptions import ContentObjectNotAvailable
from popit.models import *
from popit.tests.base_testcase import BasePopitTestCase


class LinkSerializerTestCase(BasePopitTestCase):

    def test_view_links_single(self):
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        url = person.links.untranslated().get(id="a4ffa24a9ef3cbcb8cfaa178c9329367")
        serializer = LinkSerializer(url, language="en")
        self.assertEqual(serializer.data["url"], "http://github.com/sweemeng/")

    def test_view_links_many(self):
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        url = person.links.untranslated().all()
        serializer = LinkSerializer(url, many=True, language="en")
        # TODO: This will fail, find out the exact data
        self.assertEqual(len(serializer.data), 10)

    def test_create_links(self):
        data = {
            "url": "http://twitter.com/sweemeng",
        }

        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')

        serializer = LinkSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save(content_object=person)

        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        url = person_.links.language("en").get(url="http://twitter.com/sweemeng")
        self.assertEqual(url.url, "http://twitter.com/sweemeng")

    def test_create_without_parent(self):
        data = {
            "url": "http://twitter.com/sweemeng",
        }

        serializer = LinkSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        with self.assertRaises(ContentObjectNotAvailable):
            serializer.save()

    def test_update_links(self):
        data = {
            "id": "a4ffa24a9ef3cbcb8cfaa178c9329367",
            "note": "just a random repo"
        }
        link = Link.objects.untranslated().get(id="a4ffa24a9ef3cbcb8cfaa178c9329367")
        serializer = LinkSerializer(link, data=data, partial=True, language='en')
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()

        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        url = person.links.language("en").get(id="a4ffa24a9ef3cbcb8cfaa178c9329367")
        self.assertEqual(url.note, "just a random repo")


class OtherNameSerializerTestCase(BasePopitTestCase):

    def test_view_othername_list(self):
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        other_names = person.other_names.untranslated().all()
        serializer = OtherNameSerializer(other_names, many=True, language="en")
        self.assertEqual(len(serializer.data), 1)
        self.assertEqual(serializer.data[0]["name"], "Jane")

    def test_view_othername_single(self):
        person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        other_names = person.other_names.untranslated().get(id="cf93e73f-91b6-4fad-bf76-0782c80297a8")
        serializer = OtherNameSerializer(other_names, language="en")
        self.assertEqual(serializer.data["name"], "Jane")

    def test_create_othername(self):
        data = {
            "name": "jane",
            "family_name": "jambul",
            "given_name": "test person",
            "start_date": "1950-01-01",
            "end_date": "2010-01-01",
        }
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        serializer = OtherNameSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save(content_object=person)

        person_ = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        other_name = person_.other_names.language('en').get(name="jane")
        self.assertEqual(other_name.given_name, "test person")

    def test_create_othername_without_parent(self):
        data = {
            "name": "jane",
            "family_name": "jambul",
            "given_name": "test person",
            "start_date": "1950-01-01",
            "end_date": "2010-01-01",
        }
        person = Person.objects.language('en').get(id='ab1a5788e5bae955c048748fa6af0e97')
        serializer = OtherNameSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        with self.assertRaises(ContentObjectNotAvailable):
            serializer.save()

    def test_update_othername(self):
        data = {
            "family_name": "jambul",
        }
        person = Person.objects.language('en').get(id='8497ba86-7485-42d2-9596-2ab14520f1f4')
        other_name = person.other_names.language('en').get(id="cf93e73f-91b6-4fad-bf76-0782c80297a8")
        serializer = OtherNameSerializer(other_name, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save(content_object=person)
        other_name_ = OtherName.objects.language("en").get(id="cf93e73f-91b6-4fad-bf76-0782c80297a8")
        self.assertEqual(other_name_.family_name, "jambul")


class AreaSerializerTestCase(BasePopitTestCase):

    def test_list_area(self):
        area = Area.objects.language("en").all()
        print area
        serializer = AreaSerializer(area, language="en", many=True)
        self.assertEqual(len(serializer.data), 5)

    def test_view_area(self):
        area = Area.objects.language("en").get(id="640c0f1d-2305-4d17-97fe-6aa59f079cc4")
        serializer = AreaSerializer(area, language="en")
        self.assertEqual(serializer.data["name"], "kuala lumpur")

    def test_create_area(self):
        data = {
            "name": "timbuktu"
        }
        serializer = AreaSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})

        serializer.save()
        area = Area.objects.language("en").get(name="timbuktu")
        # Just to proof that it save into database
        self.assertEqual(area.name, "timbuktu")

    def test_update_area(self):
        data = {
            "classification": "city"
        }
        area = Area.objects.untranslated().get(id="640c0f1d-2305-4d17-97fe-6aa59f079cc4")
        serializer = AreaSerializer(area, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        area = Area.objects.language("en").get(id="640c0f1d-2305-4d17-97fe-6aa59f079cc4")
        self.assertEqual(area.classification, "city")

    def test_create_area_link(self):
        data = {
            "classification": "city",
            "links": [
                {
                    "url": "http://www.google.com",
                    "note": "just a link"
                }
            ]
        }
        area = Area.objects.untranslated().get(id="640c0f1d-2305-4d17-97fe-6aa59f079cc4")
        serializer = AreaSerializer(area, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        link = area.links.language("en").get(url="http://www.google.com")
        self.assertEqual(link.note, "just a link")

    def test_update_area_link(self):
        data = {

            "links": [
                {
                    "id": "ed8a52d8-5503-45aa-a2ad-9931461172d2",
                    "note": "just a link"
                }

            ]
        }
        area = Area.objects.untranslated().get(id="640c0f1d-2305-4d17-97fe-6aa59f079cc4")
        serializer = AreaSerializer(area, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        link = area.links.language("en").get(id="ed8a52d8-5503-45aa-a2ad-9931461172d2")
        self.assertEqual(link.note, "just a link")