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
