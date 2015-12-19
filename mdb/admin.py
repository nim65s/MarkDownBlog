from django.contrib.admin import site

from .models import BlogEntry

site.register(BlogEntry)
