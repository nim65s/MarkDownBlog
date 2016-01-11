from django.conf.urls import url

from .views import (BlogEntryDetailView, BlogEntryListView, BlogEntryLongURLRedirectView,
                    BlogEntryShortURLRedirectView)

app_name = 'dmdb'
urlpatterns = [
        url(r'^(?P<yea>\d{4})/(?P<mon>\d{2})/(?P<day>\d{2})/(?P<slug>[^/]+)$',
            BlogEntryLongURLRedirectView.as_view()),
        url(r'^(?P<pk>[0-9A-F]+)$',
            BlogEntryShortURLRedirectView.as_view(), name='short'),
        url(r'^(?P<slug>[^/]+)$',
            BlogEntryDetailView.as_view(), name='entry'),
        url(r'^$',
            BlogEntryListView.as_view(), name='blog'),
        ]
