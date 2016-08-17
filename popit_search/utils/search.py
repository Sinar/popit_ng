import elasticsearch
from elasticsearch.exceptions import NotFoundError
from django.conf import settings
from django.db import models
from rest_framework.serializers import Serializer
from rest_framework.settings import api_settings
import logging
import time
from popit.models import *
from popit.serializers import *
import logging
import os
import re
import datetime
from dateutil.parser import *
from rest_framework.response import Response
from collections import OrderedDict
from urllib import urlencode
from django.core.urlresolvers import reverse
import sys
import json
from popit_search.consts import ES_MODEL_MAP
from popit_search.consts import ES_SERIALIZER_MAP

MAX_DOC_SIZE = settings.MAX_DOC_SIZE

log_path = os.path.join(settings.BASE_DIR, "log/popit_search.log")
logging.basicConfig(filename=log_path, level=logging.DEBUG)

default_date = datetime.datetime(1957, 01, 01)


# Big idea, since serializer already have json docs
class SerializerSearch(object):

    def __init__(self, doc_type=None, index=settings.ES_INDEX):
        self.es = elasticsearch.Elasticsearch(hosts=settings.ES_HOST)
        # The default parameter is for testing purposes.
        self.index = index
        self.doc_type = doc_type
        if not self.es.indices.exists(index=self.index):
            self.es.indices.create(index=self.index)
        self.page_size = api_settings.PAGE_SIZE
        self.result_count = 0
        self.start_from = 0

    def add(self, instance, serializer):
        logging.debug("Indexing %s and %s" % (str(instance), str(serializer)))
        assert isinstance(instance, models.Model)
        assert issubclass(serializer, Serializer)
        if not self.doc_type:
            raise SerializerSearchDocNotSetException("doc_type parameter need to be defined for adding")
        query = "id:%s AND language_code:%s" % (instance.id, instance.language_code)
        logging.debug("Checking index")
        result = self.es.search(index=self.index, doc_type=self.doc_type, q=query)

        hits = result["hits"]["hits"]
        if hits:
            raise SerializerSearchInstanceExist("Instance exist")
        s = serializer(instance)
        to_index = self.sanitize_data(s.data)

        result = self.es.index(index=self.index, doc_type=self.doc_type, body=to_index)
        logging.debug("Index created")
        # Can be a bad idea,
        time.sleep(settings.INDEX_PREPARATION_TIME)
        return result

    def search(self, query, language=None, start_from=0):
        # Support only query string query for now.
        # e.g https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax

        # ewww but I am on a deadline
        if "language_code" not in query and language:
            query += " AND language_code:%s" % language
        logging.warn(query)
        if not self.doc_type:
            raise SerializerSearchDocNotSetException("doc_type parameter need to be defined for search")

        result = self.es.search(index=self.index, doc_type=self.doc_type, q=query)

        hits = result["hits"]["hits"]
        output = []
        for hit in hits:
            # To return only
            output.append(hit["_source"])
        return output

    def list_all(self, page=1):
        start_from = self.get_page(int(page))
        result = self.es.search(index=self.index, from_=start_from)
        hits = result["hits"]["hits"]
        output = []
        for hit in hits:
            # To return only
            output.append(hit["_source"])
        return output

    def update(self, instance, serializer):
        assert isinstance(instance, models.Model)
        assert issubclass(serializer, Serializer)
        if not self.doc_type:
            raise SerializerSearchDocNotSetException("doc_type parameter need to be defined for update")
        query = "id:%s AND language_code:%s" % (instance.id, instance.language_code)
        result = self.es.search(index=self.index, doc_type=self.doc_type, q=query)
        hits = result["hits"]["hits"]
        if not hits:
            raise SerializerSearchNotFoundException("no result")
        if len(hits) > 1:
            raise SerializerSearchNotUniqueException("There should only have one result")
        id = hits[0]["_id"]
        serializer = serializer(instance)
        data = self.sanitize_data(serializer.data)

        result = self.es.update(index=self.index, doc_type=self.doc_type, id=id, body={"doc": data})
        time.sleep(settings.INDEX_PREPARATION_TIME)
        return result

    # delete all instance of same id. Because in ES it is stored as 2 documents
    def delete(self, instance):
        assert isinstance(instance, models.Model)
        if not self.doc_type:
            raise SerializerSearchDocNotSetException("doc_type parameter need to be defined for delete")
        query = "id:%s" % instance.id
        result = self.es.search(self.index, q=query)
        hits = result["hits"]["hits"]
        for hit in hits:
            id = hit["_id"]
            try:
                self.es.delete(index=self.index, doc_type=self.doc_type, id=id)
                time.sleep(settings.INDEX_PREPARATION_TIME)
            except NotFoundError:
                logging.warn("No index found, but it's fine")
                continue

    def delete_by_id(self, instance_id):
        if not self.doc_type:
            raise SerializerSearchDocNotSetException("doc_type parameter need to be defined for delete")
        query = "id:%s" % instance_id
        result = self.es.search(self.index, q=query)
        hits = result["hits"]["hits"]
        for hit in hits:
            id = hit["_id"]
            try:
                self.es.delete(index=self.index, doc_type=self.doc_type, id=id)
                time.sleep(settings.INDEX_PREPARATION_TIME)
            except NotFoundError:
                logging.warn("No index found, but it's fine")

    def raw_query(self, query=None):
        # Mostly for debugging, also allows for tuning of search.
        if query:
            result = self.es.search(self.index, q=query)
        else:
            result = self.es.search(self.index)
        return result

    def delete_index(self):
        self.es.indices.delete(index=self.index)

    def delete_document(self):
        if not self.doc_type:
            raise SerializerSearchDocNotSetException("doc_type parameter need to be defined for delete")
        self.es.delete(index=self.index, doc_type=self.doc_type)

    def sanitize_data(self, data):
        output = {}
        for key in data:
            if re.match("\w+_date", key):
                if data[key]:
                    new_date = parse(data[key], default=default_date)
                    output[key] = new_date.strftime("%Y-%m-%dT%H%M%S")
                else:
                    output[key] = data[key]

            elif key == "valid_from" or key == "valid_until":
                new_date = parse(data[key], default=default_date)
                output[key] = new_date.strftime("%Y-%m-%dT%H%M%S")

            elif isinstance(data[key], list):
                temp = []
                for item in data[key]:

                    temp_output = {}
                    for sub_key in item:
                        if re.match("\w+_date", sub_key):
                            if item[sub_key]:
                                new_date = parse(item[sub_key], default=default_date)
                                temp_output[sub_key] = new_date.strftime("%Y-%m-%dT%H%M%S")
                            else:
                                temp_output[sub_key] = item[sub_key]
                        elif sub_key == "valid_from" or sub_key == "valid_until":
                            if item[sub_key]:
                                new_date = parse(item[sub_key], default=default_date)
                                temp_output[sub_key] = new_date.strftime("%Y-%m-%dT%H%M%S")
                            else:
                                temp_output[sub_key] = item[sub_key]
                        else:
                            temp_output[sub_key] = item[sub_key]
                    temp.append(temp_output)
                output[key] = temp

            else:
                output[key] = data[key]
        return output

    def paginated_search(self, query, request, language=None):
        # Support only query string query for now.
        # e.g https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-query-string-query.html#query-string-syntax

        # ewww but I am on a deadline
        if "language_code" not in query and language:
            query += " AND language_code:%s" % language
        logging.warn(query)
        if not self.doc_type:
            raise SerializerSearchDocNotSetException("doc_type parameter need to be defined for search")

        # Because page from view is 1 indexed, but start_from is best calculated starting with 0
        page = request.GET.get("page", 1)
        page = int(page)
        start_from = self.get_start(page - 1)

        result = self.es.search(index=self.index, doc_type=self.doc_type, q=query, size=api_settings.PAGE_SIZE,
                                from_=start_from)

        self.result_count = result["hits"]["total"]

        hits = result["hits"]["hits"]
        output = []
        for hit in hits:
            # To return only
            output.append(hit["_source"])
        return self.response(output, request, page)

    # uurrggghh I hate it when elasticsearch do their own pagination.
    def get_page(self, item_num):
        # round it down, we start from zero anyway
        # zero index is awesome
        page = item_num / self.page_size
        if page:
            return page
        return 1

    def get_start(self, page):
        # page_size 10 * 0 first page
        # page_size 10 * 1 second page
        # 0 indexed!
        return page * self.page_size

    def has_more(self, page):
        count = page * self.page_size
        if count >= self.result_count:
            return False
        return True

    def get_next_page(self, page):
        if page * self.page_size > self.result_count:
            return None
        return page + 1

    def get_prev_page(self, page):
        if page <= 1:
            return None
        return page - 1

    def get_links(self, request, page):
        if not page:
            return None
        params = request.GET.copy()
        params["page"] = page
        url = "http://%s%s" % (request.get_host(), request.path)

        return url + "?" + urlencode(params)

    def response(self, result, request, current_page):
        """
        OrderedDict([
            ('page', int(self.page_number)),
            ('total', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data),
            ('per_page', self.page_size),
            ('num_pages', self.page.paginator.num_pages),
            ('has_more', has_more)
        ])
        :return:
        """
        num_page = self.get_page(self.result_count)
        current_page = int(current_page)
        next_page = self.get_next_page(current_page)
        next_url = self.get_links(request, next_page)
        prev_page = self.get_prev_page(current_page)
        prev_url = self.get_links(request, prev_page)
        has_more = self.has_more(current_page)

        return Response(OrderedDict([
            ("page", num_page),
            ("total", self.result_count),
            ("next", next_url),
            ("previous", prev_url),
            ("results", result),
            ("per_page", self.page_size),
            ("num_pages", num_page),
            ("has_more", has_more),
        ]))


class BulkIndexer(object):
    '''
    Data is run in this format
    {
        '_op_type': 'delete',
        '_index': 'index-name',
        '_type': 'document',
        '_id': 42,
    }
    {
        '_op_type': 'update',
        '_index': 'index-name',
        '_type': 'document',
        '_id': 42,
        'doc': {'question': 'The life, universe and everything.'}
    }

    input data is in this format
    [('persons', u'078541c9-9081-4082-b28f-29cbb64440cb', 'update'),
     ('memberships', u'b351cdc2-6961-4fc7-9d61-08fca66e1d44', 'update'),
     ('organizations', u'3d62d9ea-0600-4f29-8ce6-f7720fd49aa3', 'update'),
     ('posts', u'c1f0f86b-a491-4986-b48d-861b58a3ef6e', 'update'),
     ('memberships', u'0a44195b-c3c9-4040-8dbf-be1aa250b700', 'update'),
     ('persons', u'ab1a5788e5bae955c048748fa6af0e97', 'update'),
     ('memberships', u'7185cab2521c4f6db18b40d8d6506d36', 'update'),
     ('organizations', u'e4e9fcbf-cccf-44ff-acf6-1c5971ec85ec', 'update'),
     ('posts', u'3eb967bb-23e3-41b6-8cba-54aadac8d918', 'update'),
     ('memberships', u'62f111b2baae45edbfb2de7282580078', 'update'),
     ('persons', u'2439e472-10dc-4f9c-aa99-efddd9046b4a', 'update'),
     ('posts', u'2c6982c2-504a-4e0d-8949-dade5f9e494e', 'update'),
     ('memberships', u'b5464931-d3a9-4250-a645-204740c1bd9e', 'update'),
     ('persons', u'8497ba86-7485-42d2-9596-2ab14520f1f4', 'update'),
     ('organizations', u'612943b1-864d-4188-8d79-ca387ed19b32', 'update')]
    '''
    def __init__(self, index=settings.ES_INDEX):
        self.es = elasticsearch.Elasticsearch(hosts=settings.ES_HOST)
        self.index = index

    def index_data(self, data, max_size=MAX_DOC_SIZE):
        for item in data:

            entity_name, entity_id, ops = item
            entities = ES_MODEL_MAP[entity_name].objects.language("all").filter(id=entity_id)
            current_size = 0
            to_index = []
            for entity in entities:
                es_id = self.fetch_es_id(entity)
                serializer = ES_SERIALIZER_MAP[entity_name](entity, language=entity.language_code)
                body = serializer.data
                entry = self.create_bulk_entry(
                    es_id=es_id, doc_type=entity, ops=ops, body=body
                )
                to_index.append(entry)
                json_str = json.dumps(body)
                current_size = current_size + sys.getsizeof(json_str)
                if current_size > max_size:
                    self.es.bulk(index=self.index, body=to_index, refresh=True)
                    to_index = []
                    current_size = 0

            # To index remaining item not being index
            if to_index:
                self.es.bulk(index=self.index, body=to_index, refresh=True)

    def create_bulk_entry(self, es_id, doc_type, ops, body=None):
        if ops == "delete":
            data = {
                '_op_type': ops,
                '_index': self.index,
                '_type': doc_type,
                '_id': es_id,
            }
        elif ops == "index":
            data = {
                '_op_type': ops,
                '_index': self.index,
                '_type': doc_type,
                '_source': body
            }
        else:
            if es_id:
                data = {
                    '_op_type': ops,
                    '_index': self.index,
                    '_type': doc_type,
                    '_id': es_id,
                    '_source': body
                }
            else:
                data = {
                    '_op_type': 'index',
                    '_index': self.index,
                    '_type': doc_type,
                    '_source': body
                }

        return data

    def fetch_es_id(self, entity):
        query = "id:%s AND language:%s" % (entity.id, entity.language_code)
        result = self.es.search(index=self.index, doc_type=entity, q=query)
        _id = None
        # should have multiple id if have multiple translation
        hits = result["hits"]["hits"]

        if not hits:
            # There should only be 1 instance of data with entity.id for 1 language.
            # Only consider the first one if multiple exist, and fix the first
            _id = hits[0]["_id"]
        return _id


class SerializerSearchNotFoundException(Exception):
    pass


class SerializerSearchNotUniqueException(Exception):
    pass


class SerializerSearchInstanceExist(Exception):
    pass


class SerializerSearchDocNotSetException(Exception):
    pass


def popit_indexer(entity=""):
    count = 0
    bulk_indexer = BulkIndexer()
    if not entity or entity == "persons":
        person_indexer = SerializerSearch("persons")
        persons = Person.objects.language("all").all()
        to_index = []
        for person in persons:
            to_index.append(("persons", person.id, "create"))

    if not entity or entity == "organizations":
        org_indexer = SerializerSearch("organizations")
        to_index = []
        organizations = Organization.objects.language("all").all()
        for organization in organizations:
            to_index.append(("organizations", organization.id, "create"))

    if not entity or entity == "posts":
        post_indexer = SerializerSearch("posts")
        to_index = []
        posts = Post.objects.language("all").all()
        for post in posts:
            to_index.append(("posts", post.id, "create"))

    if not entity or entity == "memberships":
        mem_indexer = SerializerSearch("memberships")
        to_index = []
        memberships = Membership.objects.language("all").all()
        for membership in memberships:
            to_index.append(("memberships", membership.id, "create"))


def remove_popit_index():
    person_indexer = SerializerSearch("persons")
    person_indexer.delete_index()