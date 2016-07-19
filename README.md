# MarkDownBlog

The DataBase for your MarkDown Blog is just un `dbmdb` folder, where each file is a post (whose slug is the filename):

```
title: New Blog!
date: 2015-12-24
author: myself
sites: myself.com

Hey guys ! I got a new blog \o/

I can even write code in it !

    #!python

    if code.written:
        code.color()
```

## Install

`pip install -e "git://github.com/Nim65s/MarkDownBlog.git#egg=markdownblog"`

## Quick start with smdb (Static)

1. Write a `~/.config/smdb.yml` configuration file:

    ```
    site_1:
      author: John Doe
      lang: en
      links:
        - [Twitter, 'https://twitter.com/johndoe']
        - [Wikipedia, 'https://en.wikipedia.org/wiki/John_Doe']
      pages: [my_first_article]
      ssh: johndoe@jd.com
      blogtitle: JD's homepage
      url: http://jd.com/blog/
    site_2:
      author: Joe Dohn
      lang: en
      pages: [anonymous_blog_post_1]
      ssh: nobody@anonymo.us
      blogtitle: At Nobody's
      url: http://anonymo.us
    ```

2. `smdb -h` should show you what you want

## Quick start with dmdb (Django)

1. Add `"dmdb",` to your `INSTALLED_APPS`
2. Include the Django MarkDownBlog URLconf in your `urls.py`: `url(r'^blog/', include('dmdb.urls')),`
3. Run `./manage.py migrate` to create the models
4. Run `./manage.py update_blog` to update your database from your `dbmdb` folder
5. Run `./manage.py runserver` and checkout http://127.0.0.1:8000

### Optionnal: Include Sitemap in your `urls.py`:

```python
from django.contrib.sitemaps.views import index, sitemap

from dmdb.sitemaps import BlogEntrySitemap

sitemaps = {'blog': BlogEntrySitemap}

urlpatterns = [
    ...
    url(r'^sitemap\.xml$', index, {'sitemaps': sitemaps}),
    url(r'^sitemap-(?P<section>.+)\.xml$', sitemap, {'sitemaps': sitemaps}),
]
```
