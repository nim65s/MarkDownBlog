from pathlib import Path

from django.core.management.base import BaseCommand

from dmdb.models import BlogEntry, MD, DBMDB, PARSE_META, FILENAME_PATTERN


class Command(BaseCommand):
    help = "Update Django's database form the MarkDownBlog's one"

    def add_arguments(self, parser):
        parser.add_argument('dbmdb', nargs='?', type=str, default=str(DBMDB),
                help="""DataBase for MarkDownBlog: path to the folder of
                articles in markdown. Default: %s""" % DBMDB)
        parser.add_argument('-d', action='store_true',
                help="Delete other entries")

    def handle(self, *args, **options):
        dbmdb = Path(options['dbmdb'])
        for f in dbmdb.iterdir():
            with f.open('r') as fo:
                content = MD.convert(fo.read())
            b, created = BlogEntry.objects.get_or_create(slug=f.stem)
            if created:
                b.content = content
                for key, converter in PARSE_META.items():
                    if key in MD.Meta:
                        b.__dict__[key] = converter(MD.Meta[key][0])
                if 'date' not in MD.Meta:
                    try:
                        b.date = PARSE_META['date'](f.stem[:10])
                    except:
                        pass
                b.save()
                self.stdout.write('New article: %s' % b.title)
            else:
                b.update_from_file(f, self.stdout)
        for e in BlogEntry.objects.all():
            if not any(list(dbmdb.glob(p % e.slug)) for p in FILENAME_PATTERN):
                self.stdout.write('Deleted article: %s (%s)' % (e, e.slug))
                if options['d']:
                    e.delete()
