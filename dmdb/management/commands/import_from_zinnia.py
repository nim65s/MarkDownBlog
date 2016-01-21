from pathlib import Path

from django.core.management.base import BaseCommand

from dmdb.models import DBMDB
from zinnia.models import Entry


class Command(BaseCommand):
    help = 'Imports blog entries from Zinnia to the DataBase for MarkDownBlog'

    def add_arguments(self, parser):
        parser.add_argument('dbmdb', nargs='?', type=str, default=str(DBMDB),
                help="""DataBase for MarkDownBlog: path to the folder of
                articles in markdown. Default: %s""" % DBMDB)

    def handle(self, *args, **options):
        dbmdb = Path(options['dbmdb'])
        if not dbmdb.is_dir():
            dbmdb.mkdir(parents=True)

        for e in Entry.objects.all():
            with (dbmdb / ('%s.md' % e.slug)).open('w') as f:
                print('title: %s' % e.title, file=f)
                print('date: %s' % e.publication_date.date(), file=f)
                print('is_visible: %i' % e.is_visible, file=f)
                print('author: %s' % e.authors.first().username, file=f)
                print('sites: %s' % ', '.join(s.domain for s in e.sites.all()), file=f)
                print(file=f)
                print(e.content.replace('\r\n', '\n'), file=f)
