from datetime import datetime

from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse_lazy

from .models import BlogEntry


class BlogEntriesFeed(Feed):
    title = 'News'
    link = reverse_lazy('dmdb:feed')
    description = 'Latest blog entries'

    def items(self):
        return BlogEntry.objects.all()[:10]

    def item_description(self, item):
        return item.content

    def item_author_name(self, item):
        return item.author

    def item_pubdate(self, item):
        return datetime(*item.date.timetuple()[:3])

    def item_updateddate(self, item):
        return item.modification
