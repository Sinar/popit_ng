from popit_search.consts import ES_MODEL_MAP
from popit_search.consts import ES_SERIALIZER_MAP
from popit_search.utils import search, dependency


def prepare_delete(entity):
    dep_store = dependency.DependencyStore()
    dep_store.build_dependency(entity, "delete")

# Assuming instance from post_delete have enough information
def perform_delete(del_entity):
    dep_store = dependency.DependencyStore()
    graph = dep_store.fetch_dependency(del_entity)
    for node in graph:
        update_node(node)


# The reason why we have 2 phase update for delete is because we need to maintain relationship
# update, we don't have to because entity still exist
def perform_update(instance):
    graph = dependency.build_graph(instance, "update")
    for node in graph:
        update_node(node)


def update_node(node):
    entity, entity_id, action = node
    es = search.SerializerSearch(entity)
    instances = ES_MODEL_MAP[entity].objects.language("all").filter(id=entity_id)
    if not instances:
        es.delete_by_id(entity_id)
        return

    if action == "delete":
        es.delete_by_id(entity_id)
    elif action == "update":

        serializer = ES_SERIALIZER_MAP[entity]
        for instance in instances:
            es.update(instance, serializer)