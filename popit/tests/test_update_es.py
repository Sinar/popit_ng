from popit.tasks import update_node
from django.test import TestCase
from mock import patch
from popit.models import *
from popit.serializers import *


class UpdateESTask(TestCase):
    fixtures = ["api_request_test_data.yaml"]

    @patch("popit_search.utils.search.SerializerSearch")
    def test_update_node(self, mock_search):
        instance = mock_search.return_value

        node = ("organizations", "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3", "update")
        update_node(node)
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        instance.update.assert_called_with(organization, OrganizationSerializer)

    @patch("popit_search.utils.search.SerializerSearch")
    def test_delete_node(self, mock_search):
        instance = mock_search.return_value
        node = ("organizations", "3d62d9ea-0600-4f29-8ce6-f7720fd49aa3", "delete")
        update_node(node)
        instance.delete_by_id.assert_called_with("3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")