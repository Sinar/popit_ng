from django.db.models.signals import pre_delete
from django.db.models.signals import post_save
from django.db.models.signals import post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from popit.tasks import *
from popit.models import *


def entity_save_handler(sender, instance, created, raw, using, update_fields, **kwargs):
    # Raw is from loading fixtures
    if raw:
        return
    entity = instance._meta.model_name + "s"
    entity_id = instance.id
    perform_update.apply_async((entity, entity_id))


def entity_prepare_delete_handler(sender, instance, using, **kwargs):
    entity = instance._meta.model_name + "s"
    entity_id = instance.id
    prepare_delete.apply_async((entity, entity_id))


def entity_perform_delete_handler(sender, instance, using, **kwargs):
    entity = instance._meta.model_name + "s"
    entity_id = instance.id
    perform_delete.apply_async((entity, entity_id))

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, raw=False, **kwargs):
    if created and not raw:
        Token.objects.create(user=instance)


post_save.connect(entity_save_handler, sender=Person)
post_save.connect(entity_save_handler, sender=Organization)
post_save.connect(entity_save_handler, sender=Membership)
post_save.connect(entity_save_handler, sender=Post)
post_save.connect(entity_save_handler, sender=Membership)
post_save.connect(entity_save_handler, sender=ContactDetail)
post_save.connect(entity_save_handler, sender=Identifier)
post_save.connect(entity_save_handler, sender=OtherName)
post_save.connect(entity_save_handler, sender=Link)
post_save.connect(entity_save_handler, sender=Area)

pre_delete.connect(entity_prepare_delete_handler, sender=Person)
pre_delete.connect(entity_prepare_delete_handler, sender=Organization)
pre_delete.connect(entity_prepare_delete_handler, sender=Membership)
pre_delete.connect(entity_prepare_delete_handler, sender=Post)
pre_delete.connect(entity_prepare_delete_handler, sender=ContactDetail)
pre_delete.connect(entity_prepare_delete_handler, sender=Identifier)
pre_delete.connect(entity_prepare_delete_handler, sender=OtherName)
pre_delete.connect(entity_prepare_delete_handler, sender=Link)
pre_delete.connect(entity_prepare_delete_handler, sender=Area)

post_delete.connect(entity_perform_delete_handler, sender=Person)
post_delete.connect(entity_perform_delete_handler, sender=Organization)
post_delete.connect(entity_perform_delete_handler, sender=Membership)
post_delete.connect(entity_perform_delete_handler, sender=Post)
post_delete.connect(entity_perform_delete_handler, sender=ContactDetail)
post_delete.connect(entity_perform_delete_handler, sender=Identifier)
post_delete.connect(entity_perform_delete_handler, sender=OtherName)
post_delete.connect(entity_perform_delete_handler, sender=Link)
post_delete.connect(entity_perform_delete_handler, sender=Area)







