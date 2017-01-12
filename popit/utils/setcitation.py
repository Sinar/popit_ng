from popit.models import *


def set_citation_person():
    test_links = {
        "url": "http://sinarproject.org",
        "note": "this is the note for %s"
    }
    person = Person.objects.language("en").get(id="8497ba86-7485-42d2-9596-2ab14520f1f4")

    for field in person._meta.fields:
        field_name = field.attname
        if field_name == "id":
            continue

        if getattr(person, field_name):
            person.add_citation(field_name, test_links["url"], test_links["note"] % field_name)

    for field_name in person._translated_field_names:
        if field_name == "id" or field_name == "master_id" or field_name == "master":
            continue
        if getattr(person, field_name):
            person.add_citation(field_name, test_links["url"], test_links["note"] % field_name)

def set_citation_person_contact_details():
    test_links = {
        "url": "http://sinarproject.org",
        "note": "this is the note for %s"
    }
    contact_detail = ContactDetail.objects.language("en").get(id="78a35135-52e3-4af9-8c32-ea3f557354fd")

    for field in contact_detail._meta.fields:
        field_name = field.attname
        if field_name == id:
            continue
        if field_name == "object_id" or field_name == "content_object":
            continue

        contact_detail.add_citation(field_name, test_links["url"], test_links["note"] % field_name)


    for field_name in contact_detail._translated_field_names:
        if field_name == id or field_name == "master_id":
            continue
        if field_name == "object_id" or field_name == "content_object":
            continue

        if field_name == "master":
            continue

        contact_detail.add_citation(field_name, test_links["url"], test_links["note"] % field_name)


def set_citation_person_othername():
    test_links = {
        "url": "http://sinarproject.org",
        "note": "this is the note for %s"
    }
    other_name = OtherName.objects.language("en").get(id="cf93e73f-91b6-4fad-bf76-0782c80297a8")
    for field in other_name._meta.fields:
        field_name = field.attname
        if field_name == id:
            continue
        if field_name == "object_id" or field_name == "content_object":
            continue

        other_name.add_citation(field_name, test_links["url"], test_links["note"] % field_name)

    for field_name in other_name._translated_field_names:
        if field_name == id or field_name == "master_id":
            continue
        if field_name == "object_id" or field_name == "content_object":
            continue

        if field_name == "master":
            continue

        other_name.add_citation(field_name, test_links["url"], test_links["note"] % field_name)

def set_citation_person_identifier():
    test_links = {
        "url": "http://sinarproject.org",
        "note": "this is the note for %s"
    }

    identifier = Identifier.objects.language("en").get(id="2d3b8d2c-77b8-42f5-ac62-3e83d4408bda")

    for field in identifier._meta.fields:
        field_name = field.attname
        if field_name == id:
            continue
        if field_name == "object_id" or field_name == "content_object":
            continue
        identifier.add_citation(field_name, test_links["url"], test_links["note"] % field_name)

    for field_name in identifier._translated_field_names:
        if field_name == id or field_name == "master_id":
            continue
        if field_name == "object_id" or field_name == "content_object":
            continue

        if field_name == "master":
            continue

        identifier.add_citation(field_name, test_links["url"], test_links["note"] % field_name)


def set_citation_organization():
    test_links = {
        "url": "http://sinarproject.org",
        "note": "this is the note for %s"
    }
    organization = Organization.objects.language("en").get(id="3d62d9ea-0600-4f29-8ce6-f7720fd49aa3")

    for field in organization._meta.fields:
        field_name = field.attname
        if field_name == id:
            continue
        if field_name == "object_id" or field_name == "content_object":
            continue
        organization.add_citation(field_name, test_links["url"], test_links["note"] % field_name)

    for field_name in organization._translated_field_names:
        if field_name == id or field_name == "master_id":
            continue
        if field_name == "object_id" or field_name == "content_object":
            continue

        if field_name == "master":
            continue

        organization.add_citation(field_name, test_links["url"], test_links["note"] % field_name)

def set_citation_organization_othername():
    test_links = {
        "url": "http://sinarproject.org",
        "note": "this is the note for %s"
    }

    other_name = OtherName.objects.language("en").get(id="aee39ddd-6785-4a36-9781-8e745c6359b7")
    for field in other_name._meta.fields:
        field_name = field.attname
        if field_name == id:
            continue
        if field_name == "object_id" or field_name == "content_object":
            continue

        other_name.add_citation(field_name, test_links["url"], test_links["note"] % field_name)

    for field_name in other_name._translated_field_names:
        if field_name == id or field_name == "master_id":
            continue
        if field_name == "object_id" or field_name == "content_object":
            continue

        if field_name == "master":
            continue

        other_name.add_citation(field_name, test_links["url"], test_links["note"] % field_name)

def set_citation_post():
    test_links = {
        "url": "http://sinarproject.org",
        "note": "this is the note for %s"
    }

    post = Post.objects.language("en").get(id="c1f0f86b-a491-4986-b48d-861b58a3ef6e")

    for field in post._meta.fields:
        field_name = field.attname
        if field_name == id:
            continue
        if field_name == "object_id" or field_name == "content_object":
            continue
        post.add_citation(field_name, test_links["url"], test_links["note"] % field_name)

    for field_name in post._translated_field_names:
        if field_name == id or field_name == "master_id":
            continue
        if field_name == "object_id" or field_name == "content_object":
            continue

        if field_name == "master":
            continue
        post.add_citation(field_name, test_links["url"], test_links["note"] % field_name)

def set_citation_membership():
    test_links = {
        "url": "http://sinarproject.org",
        "note": "this is the note for %s"
    }

    membership = Membership.objects.language("en").get(id="b351cdc2-6961-4fc7-9d61-08fca66e1d44")

    for field in membership._meta.fields:
        field_name = field.attname
        if field_name == id:
            continue
        if field_name == "object_id" or field_name == "content_object":
            continue
        membership.add_citation(field_name, test_links["url"], test_links["note"] % field_name)

    for field_name in membership._translated_field_names:
        if field_name == id or field_name == "master_id":
            continue
        if field_name == "object_id" or field_name == "content_object":
            continue

        if field_name == "master":
            continue

        membership.add_citation(field_name, test_links["url"], test_links["note"] % field_name)