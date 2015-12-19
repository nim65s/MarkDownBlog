from django.conf.urls import url

from .views import BlogEntryListView, BlogEntryDetailView, BlogEntryShortURLRedirectView, BlogEntryLongURLRedirectView


urlpatterns = [
        url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[^/]+)$', BlogEntryLongURLRedirectView.as_view()),
        url(r'^(?P<pk>[0-9A-F]+)$', BlogEntryShortURLRedirectView.as_view(), name='short'),
        url(r'^(?P<slug>[^/]+)$', BlogEntryDetailView.as_view(), name='entry'),
        url(r'^$', BlogEntryListView.as_view(), name='blog'),
        ]
