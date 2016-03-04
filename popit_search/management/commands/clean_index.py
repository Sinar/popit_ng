from popit_search.utils.search import popit_indexer
from popit_search.utils.search import remove_popit_index
from popit_search.utils.search import SerializerSearch
from popit_search.utils.search import SerializerSearchInstanceExist
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from popit.models import *
from popit.serializers import *
import time
import logging

logging.getLogger().setLevel(logging.INFO)

MODEL_DOC_MAP = {
    "persons": Person,
    "organizations": Organization,
    "posts": Post,
    "memberships": Membership
}


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--entity", nargs="?", type=str, default="")

    def handle(self, *args, **options):

        entity = options.get("entity")
        if entity:
            if not entity in MODEL_DOC_MAP:
                logging.info("Entity %s is not in backend" % entity)
                return
            self.delete_in_es(entity)

        else:
            for entity in MODEL_DOC_MAP:
                self.delete_in_es(entity)

    def delete_in_es(self, entity):
        search = SerializerSearch(entity)
        results = search.list_all()
        for result in results:
            instance = MODEL_DOC_MAP[entity].objects.language("all").filter(id=result["id"])
            if not instance:
                search.delete_by_id(result["id"])

