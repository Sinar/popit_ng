from popit_search.utils.search import popit_indexer
from popit_search.utils.search import remove_popit_index
from popit_search.utils.search import SerializerSearch
from popit_search.utils.search import SerializerSearchInstanceExist
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from popit.models import *
from popit.serializers import *
from popit_search.consts import ES_MODEL_MAP, ES_SERIALIZER_MAP
import time
import logging

logging.getLogger().setLevel(logging.INFO)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--destroy", nargs="?", type=bool, default=True)
        parser.add_argument("--entity", nargs="?", type=str, default="")
        parser.add_argument("--entity_id", nargs="?", type=str, default="")

    def handle(self, *args, **options):
        entity = options.get("entity")
        if entity:
            entity_search = SerializerSearch(entity)
        else:
            entity_search = None
        entity_id = options.get("entity_id")

        if entity_id:
            entity_instances = ES_MODEL_MAP[entity].objects.language("all").filter(id=entity_id)
        else:
            entity_instances = []

        if options.get("destroy"):
            if entity_search:
                if entity_id:
                    for instance in entity_instances:
                        logging.info("Destroying instance of %s with %s and language %s" % (entity, entity_id, instance.language_code))
                        entity_search.delete(instance)
                        time.sleep(1)
                else:
                    logging.info("Destroying all instance of %s" % entity)
                    instances = ES_MODEL_MAP[entity].objects.language("all").all()
                    for instance in instances:
                        entity_search.delete(instance)
        else:
            logging.info("Nuclear option detected, executing. Thing could take some time")
            remove_popit_index()

        time.sleep(10)
        # Now we add
        if entity:
            if entity_id:
                for instance in entity_instances:

                    try:
                        logging.info("Add instance of %s with %s and language %s" % (entity, entity_id, instance.language_code))
                        entity_search.add(instance, ES_SERIALIZER_MAP[entity])
                        #time.sleep(1)
                    except SerializerSearchInstanceExist:
                        logging.warn("Oops instance exist in db")
                        continue
            else:
                popit_indexer(entity)
        else:
            popit_indexer(entity)
