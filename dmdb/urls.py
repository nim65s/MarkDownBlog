from django.urls import path

from .feeds import BlogEntriesFeed
from .models import BlogCategory, BlogTag
from .views import (BlogEntryDetailView, BlogEntryListView, BlogEntryLongURLRedirectView,
                    BlogEntryShortURLRedirectView, CategoryTagDetailView)

app_name = 'dmdb'
urlpatterns = [
    path('feed', BlogEntriesFeed(), name='feed'),
    path('tag/<str:slug>', CategoryTagDetailView.as_view(model=BlogTag), name='tag'),
    path('category/<str:slug>', CategoryTagDetailView.as_view(model=BlogCategory), name='category'),
    path('<int:year>/<int:month>/<int:day>/<str:slug>', BlogEntryLongURLRedirectView.as_view()),
    path('<str:pk>', BlogEntryShortURLRedirectView.as_view(), name='short'),
    path('<str:slug>', BlogEntryDetailView.as_view(), name='entry'),
    path('', BlogEntryListView.as_view(), name='blog'),
]
