# This is a way to build a set of dependency graph
from popit.models import *
from redis import Redis
from urlparse import urlparse
from django.conf import settings
import json
from django.db import models


# a dependency graph is essentially a list of tuple to show all entity
def build_graph(entity, action, memory=set()):
    graph = []
    current_object = entity._meta.model_name + "s" # Pluralize the name, i think it might fail. ES Refer object this way
    current_id = entity.id
    current_node = (current_object, current_id, action)

    # TODO: Find a more elegant way to have a stop condition
    # Not memory efficient, but I don't care I am on a schedule.
    # Big idea, if this node is processed, stop!
    if current_node in memory:
        return graph
    memory.add(current_node)
    graph.append(current_node)


    # content_type, content_object comes hand in hand
    fields = entity._meta.get_fields()
    for field in fields:
        field_name = field.name

        # The reason to check this way is because some are related object not the actual object
        if field_name in ("organization", "on_behalf_of", "parent", "person", "post", "content_object"):
            temp_entity = getattr(entity, field_name)
            if not isinstance(temp_entity, models.Model):
                continue
            if temp_entity:
                temp = build_graph(temp_entity, "update", memory=memory)
                graph.extend(temp)
        # This is a child relationship, so if parent deleted, therefore child is deleted
        elif field_name in ("memberships", "posts", "children"):
            temp_entities = getattr(entity, field_name)
            for temp_entity in temp_entities.all():
                temp = build_graph(temp_entity, action, memory=memory)
                graph.extend(temp)

    return graph


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
        print(data)
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
