from django.db.models.signals import pre_delete
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from popit.models import Person
from popit.models import Organization
from popit.models import Membership
from popit.models import Post
from popit.serializers import PersonSerializer
from popit.serializers import OrganizationSerializer
from popit.serializers import MembershipSerializer
from popit.serializers import PostSerializer
from popit_search.utils import search
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=Person)
def person_save_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    # raw is used at loading fixture. This check is so that loading fixture in unittest won't load data into elasticsearch
    if raw:
        return
    update_entity_index("persons", instance, PersonSerializer)
    for membership in instance.memberships.all():
        update_entity_index("memberships", membership, MembershipSerializer)
        if membership.organization:
            update_entity_index("organizations", membership.organization, OrganizationSerializer)
        if membership.post:
            update_entity_index("post", membership.post, PostSerializer)


# use pre_delete event is a good idea, this ensure data exist before data is emoved in indexer
@receiver(pre_delete, sender=Person)
def person_delete_handler(sender, instance, using, **kwargs):

    delete_entity_index("persons", instance)
    for membership in instance.memberships.all():
        delete_entity_index("memberships", membership)
        # keep but don't need to delete
        if membership.organization:
            update_entity_index("organizations", membership.organization, OrganizationSerializer)
        if membership.post:
            update_entity_index("post", membership.post, PostSerializer)



@receiver(post_save, sender=Organization)
def organization_save_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    if raw:
        return
    update_entity_index("organizations", instance, OrganizationSerializer)

    for post in instance.posts.all():
        update_entity_index("posts", post, PostSerializer)
    for membership in instance.memberships.all():
        update_entity_index("memberships", membership, MembershipSerializer)
        update_entity_index("persons", membership.person, PersonSerializer)


@receiver(pre_delete, sender=Organization)
def organization_delete_handler(sender, instance, using, **kwargs):
    delete_entity_index("organizations", instance)
    for post in instance.posts.all():
        delete_entity_index("posts", post)

    for membership in instance.memberships.all():
        delete_entity_index("memberships", membership)
        if membership.post:
            update_entity_index("posts", post, PostSerializer)
        update_entity_index("persons", membership.person, PersonSerializer)

    for post in instance.posts:
        delete_entity_index("posts", post)


@receiver(post_save, sender=Membership)
def membership_save_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    if raw:
        return
    update_entity_index("memberships", instance, MembershipSerializer)
    update_entity_index("persons", instance.person, PersonSerializer)
    if instance.post:
        update_entity_index("posts", instance.post, PostSerializer)
    if instance.organization:
        update_entity_index("organizations", instance.organization, OrganizationSerializer)


@receiver(pre_delete, sender=Membership)
def membership_delete_handler(sender, instance, using, **kwargs):
    delete_entity_index("memberships", instance)

@receiver(post_save, sender=Post)
def post_save_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    if raw:
        return
    update_entity_index("posts", instance, PostSerializer)
    if instance.organization:
        update_entity_index("organizations", instance.organization, OrganizationSerializer)
    for membership in instance.memberships.all():
        update_entity_index("memberships", membership, MembershipSerializer)
        update_entity_index("persons", membership.person, PersonSerializer)


@receiver(pre_delete, sender=Post)
def post_delete_handler(sender, instance, using, **kwargs):
    delete_entity_index("posts", instance)
    if instance.organization:
        update_entity_index("organizations", instance.organization, OrganizationSerializer)

    for membership in instance.memberships.all():
        delete_entity_index("memberships", membership)
        update_entity_index("persons", membership.person, PersonSerializer)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, raw=False, **kwargs):
    if created and not raw:
        Token.objects.create(user=instance)


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