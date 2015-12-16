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
    if raw:
        return
    language_code =  instance.language_code
    id = instance.id
    query = "id:%s AND language_code:%s" % (id, language_code)
    indexer = search.SerializerSearch("person")
    check = indexer.search(query, language=language_code)
    if not check:
        indexer.add(instance, PersonSerializer)
    else:
        indexer.update(instance, PersonSerializer)


# use pre_delete event is a good idea, this ensure data exist before data is emoved in indexer
@receiver(pre_delete, sender=Person)
def person_delete_handler(sender, instance, using, **kwargs):

    indexer = search.SerializerSearch("person")

    indexer.delete(instance)


@receiver(post_save, sender=Organization)
def organization_save_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    if raw:
        return
    language_code =  instance.language_code
    id = instance.id
    query = "id:%s AND language_code:%s" % (id, language_code)
    indexer = search.SerializerSearch("organization")
    check = indexer.search(query, language=language_code)
    if not check:
        indexer.add(instance, OrganizationSerializer)
    else:
        indexer.update(instance, OrganizationSerializer)


@receiver(pre_delete, sender=Organization)
def organization_delete_handler(sender, instance, using, **kwargs):
    indexer = search.SerializerSearch("organization")
    indexer.delete(instance)


@receiver(post_save, sender=Membership)
def membership_save_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    if raw:
        return
    language_code =  instance.language_code
    id = instance.id
    query = "id:%s AND language_code:%s" % (id, language_code)
    indexer = search.SerializerSearch("membership")
    check = indexer.search(query, language=language_code)
    if not check:
        indexer.add(instance, MembershipSerializer)
    else:
        indexer.update(instance, MembershipSerializer)


@receiver(pre_delete, sender=Membership)
def membership_delete_handler(sender, instance, using, **kwargs):
    indexer = search.SerializerSearch("membership")
    indexer.delete(instance)


@receiver(post_save, sender=Post)
def post_save_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    if raw:
        return
    language_code =  instance.language_code
    id = instance.id
    query = "id:%s AND language_code:%s" % (id, language_code)
    indexer = search.SerializerSearch("post")
    check = indexer.search(query, language=language_code)
    if not check:
        indexer.add(instance, PostSerializer)
    else:
        indexer.update(instance, PostSerializer)


@receiver(pre_delete, sender=Post)
def post_delete_handler(sender, instance, using, **kwargs):
    indexer = search.SerializerSearch("post")
    indexer.delete(instance)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, raw=False, **kwargs):
    if created and not raw:
        Token.objects.create(user=instance)