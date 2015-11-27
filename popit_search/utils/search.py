import elasticsearch
from django.conf import settings
from django.db import models
from rest_framework.serializers import Serializer
import logging
import time
from popit.models import *
from popit.serializers import *
import logging

INDEX_PREPARATION_TIME=5

# Big idea, since serializer already have json docs
class SerializerSearch(object):

    def __init__(self, doc_type, index=settings.ES_INDEX):
        self.es = elasticsearch.Elasticsearch(hosts=settings.ES_HOST)
        # The default parameter is for testing purposes.
        self.index = index
        self.doc_type = doc_type
        if not self.es.indices.exists(index=self.index):
            self.es.indices.create(index=self.index)

    def add(self, instance, serializer):
        assert isinstance(instance, models.Model)
        assert issubclass(serializer, Serializer)
        query = "id:%s AND language_code:%s" % (instance.id, instance.language_code)
        result = self.es.search(index=self.index, doc_type=self.doc_type, q=query)

        hits = result["hits"]["hits"]
        if hits:
            raise SerializerSearchInstanceExist("Instance exist")
        s = serializer(instance)
        result = self.es.index(index=self.index, doc_type=self.doc_type, body=s.data)
        # Can be a bad idea,
        time.sleep(INDEX_PREPARATION_TIME)
        return result

    def search(self, query, language=None):
        # Support only query string query for now.
        # e.g https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax
        result = self.es.search(self.index, q=query)
        hits = result["hits"]["hits"]
        output = []
        for hit in hits:
            # To return only
            output.append(hit["_source"])
        return output

    def update(self, instance, serializer):
        assert isinstance(instance, models.Model)
        assert issubclass(serializer, Serializer)
        query = "id:%s AND language_code:%s" % (instance.id, instance.language_code)
        result = self.es.search(index=self.index, doc_type=self.doc_type, q=query)
        hits = result["hits"]["hits"]
        if not hits:
            raise SerializerSearchNotFoundException("no result")
        if len(hits) > 1:
            raise SerializerSearchNotUniqueException("There should only have one result")
        id = hits[0]["_id"]
        serializer = serializer(instance)
        data =serializer.data

        result = self.es.update(index=self.index, doc_type=self.doc_type, id=id, body={"doc": data})
        time.sleep(INDEX_PREPARATION_TIME)
        return result

    # delete all instance of same id. Because in ES it is stored as 2 documents
    def delete(self, instance):
        assert isinstance(instance, models.Model)
        query = "id:%s" % instance.id
        result = self.es.search(self.index, q=query)
        hits = result["hits"]["hits"]
        for hit in hits:
            id = hit["_id"]
            self.es.delete(self.index, doc_type=self.doc_type, id=id)
            time.sleep(INDEX_PREPARATION_TIME)

    def raw_query(self, query):
        # Mostly for debugging, also allows for tuning of search.
        result = self.es.search(self.index, q=query)
        return result

    def delete_index(self):
        self.es.indices.delete(index=self.index)



class SerializerSearchNotFoundException(Exception):
    pass


class SerializerSearchNotUniqueException(Exception):
    pass


class SerializerSearchInstanceExist(Exception):
    pass


# TODO: Improve API usage.
def popit_indexer():
    person_indexer = SerializerSearch("person")
    persons = Person.objects.language("all").all()
    for person in persons:
        logging.warn("Indexing %s with %s for language %s" % (person.name, person.id, person.language_code))
        person_indexer.add(person, PersonSerializer)

    org_indexer = SerializerSearch("organization")
    organizations = Organization.objects.language("all").all()
    for organization in organizations:
        logging.warn("Indexing %s with %s for language %s" % (organization.name, organization.id, organization.language_code))
        org_indexer.add(organization, OrganizationSerializer)

    post_indexer = SerializerSearch("post")
    posts = Post.objects.language("all").all()
    for post in posts:
        logging.warn("Indexing %s with %s for language %s" % (post.label, post.id, post.language_code))
        post_indexer.add(post, PostSerializer)

    mem_indexer = SerializerSearch("membership")
    memberships = Membership.objects.language("all").all()
    for membership in memberships:
        logging.warn("Indexing id %s for language %s" % (membership.id, membership.language_code))
        mem_indexer.add(membership, MembershipSerializer)

def remove_popit_index():
    person_indexer = SerializerSearch("person")
    person_indexer.delete_index()