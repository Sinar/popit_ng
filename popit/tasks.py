from django.contrib.auth.models import User
from popit.models import Person
from popit.models import Organization
from popit.models import Membership
from popit.models import Post
from popit.models import OtherName
from popit.models import Identifier
from popit.models import ContactDetail
from popit.models import Link
from popit.serializers import PersonSerializer
from popit.serializers import OrganizationSerializer
from popit.serializers import MembershipSerializer
from popit.serializers import PostSerializer
from popit_search.utils import search
from celery import shared_task
from popit_search.consts import ES_MODEL_MAP
from popit_search.consts import ES_SERIALIZER_MAP
from popit_search.utils import dependency
from django.conf import settings


# Assume that the entity have enough information in es. if not it is a bug
# Sidestep all the delete handler, make frontend to filter deleted result
# Cron cleanup of staled data
@shared_task()
def index_person(instance_id):
    instances = Person.objects.language("all").filter(id=instance_id)
    for instance in instances:
        update_entity_index("persons", instance, PersonSerializer)
        for membership in instance.memberships.all():
            update_entity_index("memberships", membership, MembershipSerializer)
            if membership.organization:
                update_entity_index("organizations", membership.organization, OrganizationSerializer)
            if membership.post:
                update_entity_index("post", membership.post, PostSerializer)


@shared_task
def index_organization(instance_id):
    instances = Organization.objects.language("all").filter(id=instance_id)
    for instance in instances:
        update_entity_index("organizations", instance, OrganizationSerializer)

        for post in instance.posts.all():
            update_entity_index("posts", post, PostSerializer)
        for membership in instance.memberships.all():
            update_entity_index("memberships", membership, MembershipSerializer)
            update_entity_index("persons", membership.person, PersonSerializer)


@shared_task
def index_membership(instance_id):
    instances = Membership.objects.language("all").filter(id=instance_id)
    for instance in instances:
        update_entity_index("memberships", instance, MembershipSerializer)
        update_entity_index("persons", instance.person, PersonSerializer)
        if instance.post:
            update_entity_index("posts", instance.post, PostSerializer)
        if instance.organization:
            update_entity_index("organizations", instance.organization, OrganizationSerializer)


@shared_task
def index_post(instance_id):
    instances = Post.objects.language("all").filter(id=instance_id)
    for instance in instances:
        update_entity_index("posts", instance, PostSerializer)
        if instance.organization:
            update_entity_index("organizations", instance.organization, OrganizationSerializer)
        for membership in instance.memberships.all():
            update_entity_index("memberships", membership, MembershipSerializer)
            update_entity_index("persons", membership.person, PersonSerializer)


@shared_task
def index_othername(instance_id):
    instances = OtherName.objects.language("all").filter(id=instance_id)
    for instance in instances:
        parent = instance.content_object
        if type(parent) is Person:
            update_entity_index("persons", parent, PersonSerializer)
            for membership in parent.memberships.all():
                update_entity_index("memberships", membership, MembershipSerializer)
                if membership.organization:
                    update_entity_index("organizations", membership.organization, OrganizationSerializer)
                if membership.post:
                    update_entity_index("post", membership.post, PostSerializer)

        if type(parent) is Organization:
            update_entity_index("organizations", parent, OrganizationSerializer)

            for post in parent.posts.all():
                update_entity_index("posts", post, PostSerializer)
            for membership in parent.memberships.all():
                update_entity_index("memberships", membership, MembershipSerializer)
                update_entity_index("persons", membership.person, PersonSerializer)

        if type(parent) is Post:
            update_entity_index("posts", parent, PostSerializer)
            if parent.organization:
                update_entity_index("organizations", parent.organization, OrganizationSerializer)
            for membership in parent.memberships.all():
                update_entity_index("memberships", membership, MembershipSerializer)
                update_entity_index("persons", membership.person, PersonSerializer)


@shared_task
def index_identifier(instance_id):
    instances = Identifier.objects.language("all").filter(instance_id)
    for instance in instances:
        parent = instance.content_object

        if type(parent) is Person:
            update_entity_index("persons", parent, PersonSerializer)
            for membership in parent.memberships.all():
                update_entity_index("memberships", membership, MembershipSerializer)
                if membership.organization:
                    update_entity_index("organizations", membership.organization, OrganizationSerializer)
                if membership.post:
                    update_entity_index("post", membership.post, PostSerializer)

        if type(parent) is Organization:
            update_entity_index("organizations", parent, OrganizationSerializer)

            for post in parent.posts.all():
                update_entity_index("posts", post, PostSerializer)
            for membership in parent.memberships.all():
                update_entity_index("memberships", membership, MembershipSerializer)
                update_entity_index("persons", membership.person, PersonSerializer)


@shared_task
def index_link(instance_id):
    instances = Link.objects.language("all").filtter(instance_id)
    for instance in instances:
        parent = instance.content_object
        if type(parent) is Person:
            update_entity_index("persons", parent, PersonSerializer)
            for membership in parent.memberships.all():
                update_entity_index("memberships", membership, MembershipSerializer)
                if membership.organization:
                    update_entity_index("organizations", membership.organization, OrganizationSerializer)
                if membership.post:
                    update_entity_index("post", membership.post, PostSerializer)

        if type(parent) is Organization:
            update_entity_index("organizations", parent, OrganizationSerializer)

            for post in parent.posts.all():
                update_entity_index("posts", post, PostSerializer)
            for membership in parent.memberships.all():
                update_entity_index("memberships", membership, MembershipSerializer)
                update_entity_index("persons", membership.person, PersonSerializer)

        if type(parent) is Post:
            update_entity_index("posts", parent, PostSerializer)
            if parent.organization:
                update_entity_index("organizations", parent.organization, OrganizationSerializer)
            for membership in parent.memberships.all():
                update_entity_index("memberships", membership, MembershipSerializer)
                update_entity_index("persons", membership.person, PersonSerializer)

        if type(parent) is Membership:
            update_entity_index("memberships", parent, MembershipSerializer)
            update_entity_index("persons", parent.person, PersonSerializer)
            if parent.post:
                update_entity_index("posts", parent.post, PostSerializer)
            if parent.organization:
                update_entity_index("organizations", parent.organization, OrganizationSerializer)


@shared_task
def index_contactdetail(instance_id):
    instances = ContactDetail.objects.language("all").filter(id=instance_id)
    for instance in instances:
        parent = instance.content_object
        if type(parent) is Person:
            update_entity_index("persons", parent, PersonSerializer)
            for membership in parent.memberships.all():
                update_entity_index("memberships", membership, MembershipSerializer)
                if membership.organization:
                    update_entity_index("organizations", membership.organization, OrganizationSerializer)
                if membership.post:
                    update_entity_index("post", membership.post, PostSerializer)

        if type(parent) is Organization:
            update_entity_index("organizations", parent, OrganizationSerializer)

            for post in parent.posts.all():
                update_entity_index("posts", post, PostSerializer)
            for membership in parent.memberships.all():
                update_entity_index("memberships", membership, MembershipSerializer)
                update_entity_index("persons", membership.person, PersonSerializer)

        if type(parent) is Post:
            update_entity_index("posts", parent, PostSerializer)
            if parent.organization:
                update_entity_index("organizations", parent.organization, OrganizationSerializer)
            for membership in parent.memberships.all():
                update_entity_index("memberships", membership, MembershipSerializer)
                update_entity_index("persons", membership.person, PersonSerializer)

        if type(parent) is Membership:
            update_entity_index("memberships", parent, MembershipSerializer)
            update_entity_index("persons", parent.person, PersonSerializer)
            if parent.post:
                update_entity_index("posts", parent.post, PostSerializer)
            if parent.organization:
                update_entity_index("organizations", parent.organization, OrganizationSerializer)


# I don't trust that the serialization to work on celery
@shared_task
def prepare_delete(entity, entity_id):
    instances = ES_MODEL_MAP[entity].objects.language("all").filter(id=entity_id)
    # Do not assume that instance still exist
    if instances:
        dep_store = dependency.DependencyStore()
        if settings.INDEX_ROOT_ONLY:
            dep_store.store_root(instances[0], "delete")
        else:
            dep_store.build_dependency(instances[0], "delete")


# Assuming instance from post_delete have enough information
@shared_task
def perform_delete(entity, entity_id):
    dep_store = dependency.DependencyStore()
    graph = dep_store.fetch_graph(entity, entity_id)

    if len(graph) > 1:
        bulk_indexer = search.BulkIndexer()
        bulk_indexer.index_data(graph)
    else:
        for node in graph:
            update_node(node)


# The reason why we have 2 phase update for delete is because we need to maintain relationship
# update, we don't have to because entity still exist
@shared_task
def perform_update(entity, entity_id):
    instances = ES_MODEL_MAP[entity].objects.language("all").filter(id=entity_id)
    if settings.INDEX_ROOT_ONLY:
        graph = set()
        current_object = instances[0]._meta.model_name + "s"
        graph.add((current_object, entity_id, "update"))
    else:
        graph = dependency.build_graph(instances[0], "update")
    if len(graph) > 1:
        bulk_indexer = search.BulkIndexer()
        bulk_indexer.index_data(graph)
    else:
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
            result = es.search("id:%s" % instance.id, language=instance.language_code)
            if result:
                es.update(instance, serializer)
            else:
                es.add(instance, serializer)


def update_entity_index(name, instance, serializer):
    language_code =  instance.language_code
    id = instance.id
    query = "id:%s AND language_code:%s" % (id, language_code)
    indexer = search.SerializerSearch(name)
    check = indexer.search(query, language=language_code)
    if not check:
        indexer.add(instance, serializer)
    else:
        indexer.update(instance, serializer)


def delete_entity_index(name, instance):
    indexer = search.SerializerSearch(name)
    indexer.delete(instance)


def delete_entity_index_by_id(name, instance_id):
    indexer = search.SerializerSearch(name)
    indexer.delete_by_id(instance_id)

def search_subitem(parent, item_key, item_id):
    indexer = search.SerializerSearch(parent)
    query = "%s.id:%s" % (item_key, item_id)
    check = indexer.search(query)
    return check


def search_item(entity, entity_id, key="id"):
    indexer = search.SerializerSearch(entity)
    query = "%s:%s" % (key, entity_id)
    check = indexer.search(query)
    return check
