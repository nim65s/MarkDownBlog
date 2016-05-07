from django.contrib.admin import ModelAdmin, site

from .models import BlogCategory, BlogEntry


class BlogEntryAdmin(ModelAdmin):
    list_display = ('title', 'category')

site.register(BlogCategory)
site.register(BlogEntry, BlogEntryAdmin)
