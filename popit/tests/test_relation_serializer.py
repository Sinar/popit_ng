from popit.signals.handlers import *
from popit.models import *
from popit.serializers import RelationSerializer
import logging
from popit.tests.base_testcase import BasePopitTestCase


class RelationSerializerTestCase(BasePopitTestCase):

    def test_fetch_relation_serializer(self):
        relation = Relation.objects.untranslated().get(id="732d7ea706024973aa364b0ffa9dc2a1")
        serializer = RelationSerializer(relation, language="en")
        data = serializer.data
        self.assertEqual(data["object"]["id"], "ab1a5788e5bae955c048748fa6af0e97")
        self.assertEqual(data["subject"]["id"], "078541c9-9081-4082-b28f-29cbb64440cb")

    def test_create_relation_with_organization_serializer(self):
        data = {
            "label": "test relation",
            "object_id": "8497ba86-7485-42d2-9596-2ab14520f1f4",
            "subject_id": "078541c9-9081-4082-b28f-29cbb64440cb",
        }

        serializer = RelationSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        relation = Relation.objects.language("en").get(label="test relation")
        self.assertEqual(relation.object_id, "8497ba86-7485-42d2-9596-2ab14520f1f4")
        self.assertEqual(relation.subject_id, "078541c9-9081-4082-b28f-29cbb64440cb")

    def test_create_relation_without_subject(self):
        data = {
            "label": "test relation",
            "object_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
        }
        serializer = RelationSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_create_relation_without_object(self):
        data = {
            "label": "test relation",
            "subject_id":"8497ba86-7485-42d2-9596-2ab14520f1f4",
        }
        serializer = RelationSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_update_relation_serializer(self):
        data = {
            "label": "sweemeng land lubber"
        }
        relation = Relation.objects.untranslated().get(id="732d7ea706024973aa364b0ffa9dc2a1")
        serializer = RelationSerializer(relation, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        relation = Relation.objects.language("en").get(id="732d7ea706024973aa364b0ffa9dc2a1")
        self.assertEqual(relation.label, "sweemeng land lubber")

    def test_update_relation_create_link_serializer(self):
        data = {
            "links": [
                {
                    "url": "http://thecaptain.tumblr.com",
                    "label": "Captain's Tumblr"
                }
            ]
        }
        relation = Relation.objects.untranslated().get(id="732d7ea706024973aa364b0ffa9dc2a1")
        serializer = RelationSerializer(relation, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        link = Link.objects.language("en").get(label="Captain's Tumblr")
        self.assertEqual(link.url, "http://thecaptain.tumblr.com")

    def test_update_relation_update_link_serializer(self):
        data = {
            "links": [
                {
                    "id": "239edef4-af68-4ffb-adce-96d17cbea79d",
                    "label": "Captain's page"
                }
            ]
        }
        relation = Relation.objects.untranslated().get(id="732d7ea706024973aa364b0ffa9dc2a1")
        serializer = RelationSerializer(relation, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        link = Link.objects.language("en").get(id="239edef4-af68-4ffb-adce-96d17cbea79d")
        self.assertEqual(link.label, "Captain's page")

    def test_create_relation_invalid_date(self):
        data = {
            "label": "test relation",
            "object_id": "8497ba86-7485-42d2-9596-2ab14520f1f4",
            "subject_id": "078541c9-9081-4082-b28f-29cbb64440cb",
            "start_date": "invalid date",
            "end_date": "invalid date",
        }

        serializer = RelationSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_create_relation_valid_date(self):
        data = {
            "label": "test relation",
            "object_id": "8497ba86-7485-42d2-9596-2ab14520f1f4",
            "subject_id": "078541c9-9081-4082-b28f-29cbb64440cb",
            "start_date": "2010-01-01",
            "end_date": "2015-01-01",
        }

        serializer = RelationSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})

    def test_create_relation_invalid_object(self):
        data = {
            "label": "test relation",
            "object_id":"not_exist",
            "subject_id": "078541c9-9081-4082-b28f-29cbb64440cb",
        }

        serializer = RelationSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_create_relation_invalid_subject(self):
        data = {
            "label": "test relation",
            "object_id": "8497ba86-7485-42d2-9596-2ab14520f1f4",
            "subject_id":"not_exist",
        }

        serializer = RelationSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_update_relation_unauthorized_translated(self):
        data = {
            "label": "sweemeng adalah land lubber"
        }

        relation = Relation.objects.untranslated().get(id="732d7ea706024973aa364b0ffa9dc2a1")
        logging.warn(relation.get_available_languages())
        serializer = RelationSerializer(relation, data=data, partial=True, language="ms")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        relation = Relation.objects.language("ms").get(id="732d7ea706024973aa364b0ffa9dc2a1")
        self.assertEqual(relation.label, "Kawan Lanun")

    def test_create_relation_with_translation(self):
        data = {
            "label": "percubaan relation",
            "object_id": "8497ba86-7485-42d2-9596-2ab14520f1f4",
            "subject_id": "078541c9-9081-4082-b28f-29cbb64440cb",
        }

        serializer = RelationSerializer(data=data, language="ms")
        serializer.is_valid()
        self.assertEqual(serializer.errors, {})
        serializer.save()
        relation = Relation.objects.language("ms").get(label="percubaan relation")
        self.assertEqual(relation.object_id, "8497ba86-7485-42d2-9596-2ab14520f1f4")

    def test_create_relation_same_object_subject(self):
        data = {
            "label": "Self Relation",
            "object_id":"078541c9-9081-4082-b28f-29cbb64440cb",
            "subject_id":"078541c9-9081-4082-b28f-29cbb64440cb",
        }

        serializer = RelationSerializer(data=data, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_update_relation_replace_same_object(self):
        data = {
            "object_id": "078541c9-9081-4082-b28f-29cbb64440cb",
        }

        relation = Relation.objects.untranslated().get(id="732d7ea706024973aa364b0ffa9dc2a1")
        serializer = RelationSerializer(relation, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})

    def test_update_relation_replace_same_subject(self):
        data = {
            "subject_id": "ab1a5788e5bae955c048748fa6af0e97",
        }

        relation = Relation.objects.untranslated().get(id="732d7ea706024973aa364b0ffa9dc2a1")
        serializer = RelationSerializer(relation, data=data, partial=True, language="en")
        serializer.is_valid()
        self.assertNotEqual(serializer.errors, {})
