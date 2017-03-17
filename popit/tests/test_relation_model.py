from django.core.exceptions import ValidationError
from popit.models import *
from popit.tests.base_testcase import BasePopitTestCase


class RelationModelTestCase(BasePopitTestCase):

    def test_create_relation(self):
        subject = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        object = Person.objects.language("en").get(id="078541c9-9081-4082-b28f-29cbb64440cb")
        relation = Relation.objects.language("en").create(
            subject=subject,
            object=object,
        )
        self.assertEqual(relation.subject_id, "8497ba86-7485-42d2-9596-2ab14520f1f4")
        self.assertEqual(relation.object_id, "078541c9-9081-4082-b28f-29cbb64440cb")

    def test_create_relation_without_subject(self):
        object = Person.objects.language("en").get(id="078541c9-9081-4082-b28f-29cbb64440cb")
        with self.assertRaises(ValidationError):
            Relation.objects.language("en").create(
                object=object,
            )

    def test_create_relation_without_object(self):
        subject = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        with self.assertRaises(ValidationError):
            Relation.objects.language("en").create(
                subject=subject,
            )

    def test_create_relation_full(self):
        subject = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        object = Person.objects.language("en").get(id="078541c9-9081-4082-b28f-29cbb64440cb")
        relation=Relation.objects.language("en").create(
            label="Test full relation",
            start_date="2010-01-01",
            end_date="2016-01-01",
            subject=subject,
            object=object,
        )
        self.assertEqual(relation.subject_id, "8497ba86-7485-42d2-9596-2ab14520f1f4")
        self.assertEqual(relation.object_id, "078541c9-9081-4082-b28f-29cbb64440cb")

    def test_create_relation_links(self):
        relation = Relation.objects.language("en").get(id="732d7ea706024973aa364b0ffa9dc2a1")
        Link.objects.language("en").create(
            url="http://facebook.com/scaly_wag",
            content_object=relation
        )

        links = relation.links.language("en").get(url="http://facebook.com/scaly_wag")
        self.assertEqual(links.url, "http://facebook.com/scaly_wag")

    def test_create_bad_date_relation(self):
        subject = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")
        object = Person.objects.language("en").get(id="078541c9-9081-4082-b28f-29cbb64440cb")
        with self.assertRaises(ValidationError):
            relation=Relation.objects.language("en").create(
                label="Test full relation",
                start_date="abcd",
                end_date="abcd",
                subject=subject,
                object=object,
            )
