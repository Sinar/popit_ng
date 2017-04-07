# This is a way to build a set of dependency graph
from popit.models import *
from redis import Redis
from urlparse import urlparse
from django.conf import settings
import json
from django.db import models


# a dependency graph is essentially a list of tuple to show all entity
def build_graph(entity, action):
    graph = set()

    current_object = entity._meta.model_name + "s"  # Pluralize the name, ES Refer object this way
    current_id = entity.id
    current_node = (current_object, current_id, action)

    graph.add(current_node)

    # this should show all field that show relationship, foreign key and what not
    # I don't care about translated field, the goal is to traverse through relationship
    fields = entity._meta.get_fields()

    for field in fields:
        field_name = field.name
        if field_name in ("organization", "on_behalf_of", "parent", "person", "object", "subject", "post", "content_object"):
            temp_entity = getattr(entity, field_name)
            if not isinstance(temp_entity, models.Model):
                continue
            if temp_entity:
                current_node = (temp_entity._meta.model_name + "s", temp_entity.id, "update")
                graph.add(current_node)

        elif field_name == "memberships":
            temp_entities = getattr(entity, field_name)
            for temp_entity in temp_entities.all():
                # add current item to be index
                current_node = ("memberships", temp_entity.id, action)
                graph.add(current_node)

                # Now membership have organization, person, post or both
                person_node = ("persons", temp_entity.person.id, "update")
                graph.add(person_node)

                # It might not have, because post have org. We kind of automatically populate it, except for old entry
                if temp_entity.organization:
                    org_node = ("organizations", temp_entity.organization_id, "update")
                    graph.add(org_node)

                if temp_entity.post:
                    post_node = ("posts", temp_entity.post_id, "update")
                    graph.add(post_node)

        elif field_name in ("relations_as_object", "relations_as_subject"):
            temp_entities = getattr(entity, field_name)
            for temp_entity in temp_entities.all():
                # add current item to be index
                current_node = ("relations", temp_entity.id, action)
                graph.add(current_node)

                # Relations have two persons
                object_node = ("persons", temp_entity.object.id, action)
                subject_node = ("persons", temp_entity.subject.id, action)
                graph.add(object_node)
                graph.add(subject_node)

        elif field_name in ("posts", "children"): # For post and children org just index this post or org
            temp_entities = getattr(entity, field_name)
            for temp_entity in temp_entities.all():
                current_node = (temp_entity._meta.model_name + "s", temp_entity.id, action)
                graph.add(current_node)

    return list(graph)


class DependencyStore(object):
    def __init__(self):
        uri = settings.ES_DATA_BIN
        parsed_uri = urlparse(uri)

        self.store = Redis(
            host = parsed_uri.hostname,
            port = parsed_uri.port,
            db=parsed_uri.path[1:], #because it returns in /:dbnumber
        )

    def store_graph(self, entity, entity_id, graph):
        data = json.dumps(graph)
        key = "%s, %s" % (entity, entity_id)
        self.store.set(key, data)

    def fetch_graph(self, entity, entity_id):
        key = "%s, %s" % (entity, entity_id)
        data = self.store.get(key)
        if data:
            return json.loads(data)
        # Graph is a list. Silent error is bad, but in this case, if entity is already deleted I don't care
        # https://docs.djangoproject.com/en/1.9/ref/models/querysets/#delete
        # The delete() method does a bulk delete and does not call any delete() methods on your models.
        # It does, however, emit the pre_delete and post_delete signals for all deleted objects (including cascaded deletions).
        return []

    def build_dependency(self, entity, action):
        name = entity._meta.model_name
        id_ = entity.id
        graph = build_graph(entity, action)
        self.store_graph(name, id_, graph)

    def fetch_dependency(self, entity):
        name = entity._meta.model_name
        id_ = entity.id
        graph = self.fetch_graph(name, id_)
        return graph
