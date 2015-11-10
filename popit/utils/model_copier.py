from popit.models import Contact
from popit.models import ContactDetail
from popit.models import Link

# This is a one time script that I used for migrating Contact to ContactDetails
def contact_copier():
    for language in ("en", "ms"):
        source = Contact.objects.language(language).all()
        for item in source:
            try:
                destination = ContactDetail.objects.language(language).get(id=item.id)
                destination.type = item.type
                destination.value = item.value
                destination.valid_from = item.valid_from
                destination.valid_until = item.valid_until
                destination.object_id = item.object_id
                destination.content_type = item.content_type
                destination.content_object = item.content_object
                destination.created_at = item.created_at
                destination.updated_at = item.updated_at
                destination.label = item.label
                destination.note = item.note
                destination.save()
            except ContactDetail.DoesNotExist:
                data = {}
                data["id"] = item.id
                data["value"] = item.value
                data["type"] = item.type
                data["valid_from"] = item.valid_from
                data["valid_until"] = item.valid_until
                data["object_id"] = item.object_id
                data["content_type"] = item.content_type
                data["content_object"] = item.content_object
                data["created_at"] = item.created_at
                data["updated_at"] = item.updated_at
                data["note"] = item.note
                data["label"] = item.label
                destination = ContactDetail.objects.language(language).create(
                    **data
                )
            links = Link.objects.language(language).filter(object_id=item.id)
            for link in links:
                link.content_object = destination
                link.save()
