from popit_search.utils.search import popit_indexer
from popit_search.utils.search import remove_popit_index
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
import time


class Command(BaseCommand):
    def handle(self, *args, **options):
        remove_popit_index()
        time.sleep(10)
        popit_indexer()