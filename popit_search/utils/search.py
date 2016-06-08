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

    def list_all(self):
        result = self.es.search(index=self.index)
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

            elif type(data[key]) is list:
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
    if not entity or entity == "persons":
        person_indexer = SerializerSearch("persons")
        persons = Person.objects.language("all").all()
        for person in persons:
            try:
                logging.warn("Indexing %s with %s for language %s" % (person.name, person.id, person.language_code))
                count = count + 1
                status=person_indexer.add(person, PersonSerializer)
                logging.warn(status)
            except SerializerSearchInstanceExist:
                logging.warn("Instance %s with %s for language %s exist" % (person.name, person.id, person.language_code))

    if not entity or entity == "organizations":
        org_indexer = SerializerSearch("organizations")
        organizations = Organization.objects.language("all").all()
        for organization in organizations:
            try:
                logging.warn("Indexing %s with %s for language %s" % (organization.name, organization.id, organization.language_code))
                count = count + 1
                status=org_indexer.add(organization, OrganizationSerializer)
                logging.warn(status)
            except SerializerSearchInstanceExist:
                logging.warn("Instance %s with %s for language %s exist" % (organization.name, organization.id, organization.language_code))

    if not entity or entity == "posts":
        post_indexer = SerializerSearch("posts")
        posts = Post.objects.language("all").all()
        for post in posts:
            try:
                logging.warn("Indexing %s with %s for language %s" % (post.label, post.id, post.language_code))
                count = count + 1
                status=post_indexer.add(post, PostSerializer)
                logging.warn(status)
            except SerializerSearchInstanceExist:
                logging.warn("Instance %s with %s for language %s exist" % (post.label, post.id, post.language_code))

    if not entity or entity == "memberships":
        mem_indexer = SerializerSearch("memberships")
        memberships = Membership.objects.language("all").all()
        for membership in memberships:
            try:
                logging.warn("Indexing id %s for language %s" % (membership.id, membership.language_code))
                count = count + 1
                status=mem_indexer.add(membership, MembershipSerializer)
                logging.warn(status)
            except SerializerSearchInstanceExist:
                logging.warn("Instance with %s for language %s exist" % (membership.id, membership.language_code))


def remove_popit_index():
    person_indexer = SerializerSearch("persons")
    person_indexer.delete_index()