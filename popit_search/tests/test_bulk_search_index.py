from mock import patch
from django.test import TestCase
from popit_search.utils import search
from popit_search.consts import ES_SERIALIZER_MAP
from popit_search.consts import ES_MODEL_MAP
from popit.models import *
from popit.serializers import *


class BulkIndexTestCase(TestCase):
    fixtures = ["api_request_test_data.yaml"]

    @patch("elasticsearch.Elasticsearch")
    def test_generate_bulk_update_entry(self, mock_search):

        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, language="en")
        body = serializer.data
        es_id = 1
        doc_type = "organizations"
        bulk_indexer = search.BulkIndexer("popit")
        entry = bulk_indexer.create_bulk_entry(
            es_id,
            doc_type,
            "update",
            body
        )

        self.assertEqual(entry["_id"], es_id)
        # Pick field to test, it is not exactly the same object
        self.assertEqual(entry["_op_type"], "update")
        # Because only index/create use _source update uses doc
        self.assertEqual(entry["doc"]["id"], body["id"])
        self.assertEqual(entry["doc"]["name"], body["name"])

    @patch("elasticsearch.Elasticsearch")
    def test_generate_bulk_delete_entry(self, mock_search):

        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, language="en")
        body = serializer.data
        es_id = 1
        doc_type = "organizations"
        bulk_indexer = search.BulkIndexer("popit")
        entry = bulk_indexer.create_bulk_entry(
            es_id,
            doc_type,
            "delete",
            body
        )
        self.assertEqual(entry["_id"], es_id)
        self.assertEqual(entry["_op_type"], "delete")
        self.assertFalse("_source" in entry)

    @patch("elasticsearch.Elasticsearch")
    def test_generate_bulk_create_entry(self, mock_search):
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        serializer = OrganizationSerializer(organization, language="en")
        body = serializer.data
        es_id = None
        doc_type = "organizations"
        bulk_indexer = search.BulkIndexer("popit")
        entry = bulk_indexer.create_bulk_entry(
            es_id,
            doc_type,
            "update",
            body
        )

        self.assertEqual(entry["_op_type"], "index")
        self.assertFalse("_id" in entry)
