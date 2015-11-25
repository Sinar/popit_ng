# TODO: Implement for each
from django.db.models.signals import pre_delete
from django.db.models.signals import post_save
from django.dispatch import receiver
from popit.models import Person
from popit.models import Organization
from popit.models import Membership
from popit.models import Post
from popit.serializers import PersonSerializer
from popit.serializers import OrganizationSerializer
from popit.serializers import MembershipSerializer
from popit.serializers import PostSerializer
from popit_search.utils import search


@receiver(post_save, sender=Person)
def person_save_handler(sender, **kwargs):
    language_code =  sender.language_code
    id = sender.id
    query = "id:%s AND language_code:%s" % (id, language_code)
    indexer = search.SerializerSearch("person")
    check = indexer.search(query, language=language_code)
    if not check:
        indexer.add(sender, PersonSerializer)
    else:
        indexer.update(sender, PersonSerializer)


# use pre_delete event is a good idea, this ensure data exist before data is emoved in indexer
@receiver(pre_delete, sender=Person)
def person_delete_handler(sender, **kwargs):

    indexer = search.SerializerSearch("person")

    indexer.delete(sender)


@receiver(post_save, sender=Organization)
def organization_save_handler(sender, **kwargs):
    language_code =  sender.language_code
    id = sender.id
    query = "id:%s AND language_code:%s" % (id, language_code)
    indexer = search.SerializerSearch("organization")
    check = indexer.search(query, language=language_code)
    if not check:
        indexer.add(sender, OrganizationSerializer)
    else:
        indexer.update(sender, OrganizationSerializer)


@receiver(pre_delete, sender=Organization)
def organization_delete_handler(sender, **kwargs):
    indexer = search.SerializerSearch("organization")
    indexer.delete(sender)


@receiver(post_save, sender=Membership)
def membership_save_handler(sender, **kwargs):
    language_code =  sender.language_code
    id = sender.id
    query = "id:%s AND language_code:%s" % (id, language_code)
    indexer = search.SerializerSearch("membership")
    check = indexer.search(query, language=language_code)
    if not check:
        indexer.add(sender, MembershipSerializer)
    else:
        indexer.update(sender, MembershipSerializer)


@receiver(pre_delete, sender=Membership)
def membership_delete_handler(sender, **kwargs):
    indexer = search.SerializerSearch("membership")
    indexer.delete(sender)


@receiver(post_save, sender=Post)
def post_save_handler(sender, **kwargs):
    language_code =  sender.language_code
    id = sender.id
    query = "id:%s AND language_code:%s" % (id, language_code)
    indexer = search.SerializerSearch("post")
    check = indexer.search(query, language=language_code)
    if not check:
        indexer.add(sender, PostSerializer)
    else:
        indexer.update(sender, PostSerializer)


@receiver(pre_delete, sender=Post)
def post_delete_handler(sender, **kwargs):
    indexer = search.SerializerSearch("post")
    indexer.delete(sender)