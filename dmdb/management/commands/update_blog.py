from django.core.management.base import BaseCommand

from dmdb.models import BlogEntry, DBMDB


class Command(BaseCommand):
    help = "Update Django's database form the MarkDownBlog's one"

    def add_arguments(self, parser):
        parser.add_argument('dbmdb', nargs='?', type=str, default=str(DBMDB),
                help="""DataBase for MarkDownBlog: path to the folder of
                articles in markdown. Default: %s""" % DBMDB)
        parser.add_argument('-d', action='store_true',
                help="Delete other entries")

    def handle(self, *args, **options):
        BlogEntry.update_all(path=options['dbmdb'], delete=options['d'])
