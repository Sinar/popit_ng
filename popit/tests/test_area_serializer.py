from django.test import TestCase
from popit.serializers import AreaSerializer
from popit.models import Area


class AreaSerializerTestCase(TestCase):

    fixtures = [ "api_request_test_data.yaml" ]

    def test_create_area(self):
        data = {
            "name":"petaling jaya",
            "classification": "town"
        }
        serializer = AreaSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        area = Area.objects.language("en").get(name="petaling jaya")
        self.assertEqual(area.classification, "town")

    def test_fetch_area(self):
        area = Area.objects.untranslated().get(id="b0c2dbaba8ea476f91db1e3c2320dcb7")
        serializer = AreaSerializer(area, language="en")
        data = serializer.data
        self.assertEqual(data["name"], "Subang Jaya")

    def test_update_area(self):
        data = {
            "identifier": "P21"
        }
        area = Area.objects.untranslated().get(id="b0c2dbaba8ea476f91db1e3c2320dcb7")
        serializer = AreaSerializer(area, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        area = Area.objects.language("en").get(id="b0c2dbaba8ea476f91db1e3c2320dcb7")

        self.assertEqual(area.identifier, "P21")

    def test_fetch_area_translated_serializer(self):
        area = Area.objects.untranslated().get(id="b0c2dbaba8ea476f91db1e3c2320dcb7")
        serializer = AreaSerializer(area, language="ms")
        data = serializer.data
        self.assertEqual(data["language_code"], "ms")

    def test_create_area_translated(self):
        data = {
            "name": "petaling jaya",
            "classification": "bandar"
        }
        serializer = AreaSerializer(data=data, language="ms")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        area = Area.objects.language("ms").get(name="petaling jaya")
        self.assertEqual(area.classification, "bandar")

    def test_update_area_translated(self):
        data = {
            "name": "Subang Jaya",
            "classification": "bandar"
        }
        area = Area.objects.untranslated().get(id="b0c2dbaba8ea476f91db1e3c2320dcb7")
        serializer = AreaSerializer(area, data=data, language="ms", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        area = Area.objects.language("ms").get(id="b0c2dbaba8ea476f91db1e3c2320dcb7")
        self.assertEqual(area.classification, "bandar")






