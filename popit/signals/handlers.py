from django.db.models.signals import pre_delete
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from popit.tasks import *


@receiver(post_save, sender=Person)
def person_save_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    # raw is used at loading fixture. This check is so that loading fixture in unittest won't load data into elasticsearch
    if raw:
        return
    instance_id = instance.id
    index_person.apply_async((instance_id, ))

@receiver(post_save, sender=Organization)
def organization_save_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    if raw:
        return
    instance_id = instance.id
    index_organization.apply_async((instance_id, ))

@receiver(post_save, sender=Membership)
def membership_save_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    if raw:
        return
    instance_id = instance.id
    index_membership.apply_async((instance_id, ))

@receiver(post_save, sender=Post)
def post_save_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    if raw:
        return

    instance_id = instance.id
    index_post.apply_async((instance_id, ))

@receiver(post_save, sender=OtherName)
def othername_save_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    if raw:
        return
    instance_id = instance.id
    index_othername.apply_async((instance_id,))

@receiver(post_save, sender=Identifier)
def identifier_save_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    if raw:
        return

    instance_id = instance.id
    index_identifier.apply_async((instance_id,))

@receiver(post_save, sender=Link)
def link_save_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    if raw:
        return
    instance_id = instance.id
    index_link.apply_async((instance_id,))


@receiver(post_save, sender=ContactDetail)
def contactdetail_save_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    if raw:
        return

    instance_id = instance.id
    index_contactdetail.apply_async((instance_id,))

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