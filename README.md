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

## Quick start with smdb (Static)

## Quick start with dmdb (Django)

1. Add "dmdb" to your `INSTALLED_APPS`
2. Include the Django MarkDownBlog URLconf in your `urls.py`: `url(r'^blog/', include('dmdb.urls')),`
3. Run `./manage.py migrate` to create the models
4. Run `./manage.py update_blog` to update your database from your `dbmdb` folder
5. Run `./manage.py runserver` and checkout http://127.0.0.1:8000
