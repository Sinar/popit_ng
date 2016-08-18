# TODO: Check if all entity in graph valid
# TODO: Check if it have generated all the sub item. (Tough one)
# TODO: Make sure the call is valid(might be the other test, it is currently inside popit.task)
from popit.models import *
from popit_search.utils import dependency
from django.test import TestCase
from popit_search import consts


class DependencyGraphTestCase(TestCase):
    fixtures = [ "api_request_test_data.yaml" ]

    def test_instance_exist_from_graph(self):
        # It can be any language version, the foreign key are not translated, why would they?
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        graph = dependency.build_graph(organization, "update")

        for node in graph:
            entity, entity_id, action = node

            instances = consts.ES_MODEL_MAP[entity].objects.language("all").filter(id=entity_id)
            self.assertTrue(instances)

    def test_instance_exist_in_graph(self):
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        graph = dependency.build_graph(organization, "update")
        memory = set(graph)

        # Just a sample of what is in the the graph is good enough
        for membership in organization.memberships.all():
            node = ("memberships", membership.id, "update")
            self.assertTrue(node in memory)

            person = ("persons", membership.person_id, "update")

            self.assertTrue(person in memory)
            if membership.post_id:
                post = ("posts", membership.post_id, "update")
                self.assertTrue(post in memory)

    def test_delete_action(self):
        organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")
        graph = dependency.build_graph(organization, "delete")
        memory = set(graph)

        for membership in organization.memberships.all():
            node = ("memberships", membership.id, "delete")
            self.assertTrue(node in memory)

            if membership.post_id:
                post = ("posts", membership.post_id, "delete")
                self.assertTrue(post in memory)