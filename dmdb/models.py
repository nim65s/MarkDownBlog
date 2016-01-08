from datetime import datetime, date
from difflib import Differ
from pathlib import Path
import sys

from django.conf import settings
from django.db.models import Model, DateField, CharField, BooleanField, TextField, ManyToManyField, Manager
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse

from markdown import Markdown


DBMDB = Path(settings.BASE_DIR) / 'dbmdb'
DIFFER = Differ()
MD = Markdown(output_format='html5', extensions=[
    'markdown.extensions.codehilite',
    'markdown.extensions.meta',
    'markdown.extensions.nl2br',
    'markdown.extensions.sane_lists',
    ])
PARSE_META = {
        'title': lambda x: x,
        'date': lambda x: datetime.strptime(x, '%Y-%m-%d').date(),
        'is_visible': lambda x: bool(int(x)),
        'author': lambda x: x,
        'template': lambda x: x,
        }
FILENAME_PATTERN = ['%s', '%s.md', '%s.markdown',
        '*-*-*%s', '*-*-*%s.md', '*-*-*%s.markdown']


class BlogEntry(Model):
    slug = CharField(max_length=200, unique=True)
    title = CharField(max_length=200)
    date = DateField(default=date.today)
    is_visible = BooleanField(default=True)
    content = TextField()
    author = CharField(max_length=100)
    sites = ManyToManyField(Site, default=get_current_site)
    template = CharField(max_length=50, default='post')

    objects = Manager()
    on_site = CurrentSiteManager()

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('dmdb:entry', kwargs={'slug': self.slug})

    def get_short_url(self):
        return reverse('dmdb:short', kwargs={'pk': hex(self.pk)})

    def update_from_file(self, path, created=False, stdout=sys.stdout):
        with path.open('r') as f:
            content = MD.convert(f.read())
        if content != self.content:
            if not created:
                stdout.writelines(DIFFER.compare(self.content, content))
            self.content = content
        for key, converter in PARSE_META.items():
            if key in MD.Meta:
                old, new = self.__dict__[key], converter(MD.Meta[key][0])
                if old != new:
                    if not created:
                        stdout.write('Changed %s: %s → %s' % (key, old, new))
                    self.__dict__[key] = new
        for domain in map(str.strip, MD.Meta['sites'][0].split(',')):
            site, created = Site.objects.get_or_create(domain=domain)
            if created:
                stdout.write('New site: %s' % domain)
                site.name = domain
            self.sites.add(site)
        if created:
            self.stdout.write('New article: %s' % b.title)
        self.save()

    @staticmethod
    def update_all(self, dbmdb=DBMDB, delete=False, stdout=sys.stdout):
        dbmdb = Path(dbmdb)
        for f in dbmdb.glob('*.md'):
            b, created = BlogEntry.objects.get_or_create(slug=f.stem)
            b.update_from_file(f, created, stdout)
        for e in BlogEntry.objects.all():
            if not any(list(dbmdb.glob(p % e.slug)) for p in FILENAME_PATTERN):
                message = 'Deleted' if delete else 'Missing'
                stdout.write('%s article: %s (%s)' % (message, e, e.slug))
                if delete:
                    e.delete()
