import requests
from urlparse import urljoin
from popit_search.consts import ES_SERIALIZER_MAP, ES_MODEL_MAP
from popit.models import *
from popit_search.utils import search

ES_URL = "10.8.0.1/popit/%s/_search/"


def clean_data():
    processed = set()
    for key in ES_SERIALIZER_MAP:
        url = ES_URL % key
        entities = ES_MODEL_MAP[key].objects.language("all").all()
        for entity in entities:
            # `
            query = "id:%s AND language_code:%s" % (entity.id, entity.language_code)
            r = requests.get(url, params={"q":query})
            data = r.json()
            for hit in data["hits"]["hits"]:
                es_id = hit["_id"]

                source = hit["_source"]

