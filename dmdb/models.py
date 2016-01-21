import sys
from datetime import date
from pathlib import Path

from django.conf import settings
from django.contrib.sites.managers import CurrentSiteManager
from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.db.models import BooleanField, CharField, DateField, Manager, ManyToManyField, Model, TextField

from mdb_settings import DIFFER, FILENAME_PATTERN, MD, META, readlines

DBMDB = Path(settings.BASE_DIR) / 'dbmdb'


class BlogEntry(Model):
    slug = CharField(max_length=200, unique=True)
    title = CharField(max_length=200)
    date = DateField(default=date.today)
    is_visible = BooleanField(default=True)
    content = TextField()
    author = CharField(max_length=100)
    sites = ManyToManyField(Site, default=get_current_site)
    template = CharField(max_length=50, default='post')
    lang = CharField(max_length=2, default='en')

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

    def update_sites(self, domains, created=False, stdout=sys.stdout):
        for domain in domains:
            site, site_created = Site.objects.get_or_create(domain=domain)
            if site_created:
                site.name = domain
                site.save()
                stdout.write('New site: %s; please change its name\n' % site)
            self.sites.add(site)
        if not created:
            for site in self.sites.all():
                if site.domain not in domains:
                    self.sites.remove(site)
                    stdout.write('Article %s not on %s anymore\n' % (self, site))

    def update_from_file(self, path, created=False, stdout=sys.stdout):
        stdout.write('\n* %s\n' % path)
        with path.open('r') as f:
            content = MD.convert(f.read())
        if content != self.content:
            if not created:
                stdout.writelines(DIFFER.compare(readlines(self.content), readlines(content)))
            self.content = content
        for key, converter in META.items():
            if key in MD.Meta:
                old, new = self.__dict__[key], converter(MD.Meta[key][0])
                if old != new:
                    if not created:
                        stdout.write('Changed %s: %s → %s\n' % (key, old, new))
                    self.__dict__[key] = new
        if 'sites' in MD.Meta:
            domains = list(map(str.strip, MD.Meta['sites'][0].split(',')))
            self.update_sites(domains, created, stdout)
        MD.reset()
        self.save()

    @staticmethod
    def update_all(dbmdb=DBMDB, delete=False, stdout=sys.stdout):
        dbmdb = Path(dbmdb)
        for f in dbmdb.glob('*.md'):
            b, created = BlogEntry.objects.get_or_create(slug=f.stem)
            if created:
                stdout.write('New article: %s' % b.title)
            b.update_from_file(f, created, stdout)
        for e in BlogEntry.objects.all():
            if not any(list(dbmdb.glob(p % e.slug)) for p in FILENAME_PATTERN):
                message = 'Deleted' if delete else 'Missing'
                stdout.write('%s article: %s (%s)\n' % (message, e, e.slug))
                if delete:
                    e.delete()
