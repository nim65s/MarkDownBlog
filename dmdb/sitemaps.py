from django.contrib.sitemaps import Sitemap

from .models import BlogEntry


class BlogEntrySitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.6
    protocol = 'https'

    def items(self):
        return BlogEntry.on_site.filter(is_visible=True)

    def lastmod(self, item):
        return item.modification
