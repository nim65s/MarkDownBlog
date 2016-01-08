from django.core.management.base import BaseCommand

from dmdb.models import BlogEntry, DBMDB
from mdb_settings import parser_args


class Command(BaseCommand):
    help = "Update Django's database form the MarkDownBlog's one"

    def add_arguments(self, parser):
        parser_args(parser, DBMDB)

    def handle(self, *args, **options):
        BlogEntry.update_all(dbmdb=options['dbmdb'], delete=options['delete'])
