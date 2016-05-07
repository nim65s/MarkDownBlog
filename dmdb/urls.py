from django.conf.urls import url

from .feeds import BlogEntriesFeed
from .models import BlogCategory, BlogTag
from .views import (BlogEntryDetailView, BlogEntryListView, BlogEntryLongURLRedirectView,
                    BlogEntryShortURLRedirectView, CategoryTagDetailView)

app_name = 'dmdb'
urlpatterns = [
    url(r'^feed$', BlogEntriesFeed(), name='feed'),
    url(r'^tag/(?P<slug>[^/]+)$', CategoryTagDetailView.as_view(model=BlogTag), name='tag'),
    url(r'^category/(?P<slug>[^/]+)$', CategoryTagDetailView.as_view(model=BlogCategory), name='category'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[^/]+)$', BlogEntryLongURLRedirectView.as_view()),
    url(r'^(?P<pk>[0-9A-F]+)$', BlogEntryShortURLRedirectView.as_view(), name='short'),
    url(r'^(?P<slug>[^/]+)$', BlogEntryDetailView.as_view(), name='entry'),
    url(r'^$', BlogEntryListView.as_view(), name='blog'),
]
