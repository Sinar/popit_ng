from popit.serializers import AreaSerializer
from popit.models import Area
from popit.tests.base_testcase import BasePopitTestCase


class AreaSerializerTestCase(BasePopitTestCase):

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

    def test_parent_area_exist(self):
        area = Area.objects.untranslated().get(id="802be15a7483442ab9ecd521410269fa")
        serializer = AreaSerializer(area, language="en")

        data = serializer.data
        self.assertTrue("parent" in data)
        self.assertEqual(data["parent"]["id"], "5ea50458870942b1b2ed2370fa9c779b")

    def test_children_area_exist(self):
        area = Area.objects.untranslated().get(id="5ea50458870942b1b2ed2370fa9c779b")
        serializer = AreaSerializer(area, language="en")

        data = serializer.data
        self.assertTrue("children" in data)
        test_list = []
        for i in data["children"]:
            test_list.append(i["id"])

        self.assertTrue("802be15a7483442ab9ecd521410269fa" in test_list)

    def test_set_parent_area_null(self):
        data = {
            "parent_id": None
        }

        area = Area.objects.untranslated().get(id="802be15a7483442ab9ecd521410269fa")
        serializer = AreaSerializer(area, data=data, language="en", partial=True)
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()

        area = Area.objects.language("en").get(id="802be15a7483442ab9ecd521410269fa")
        self.assertEqual(area.parent, None)
