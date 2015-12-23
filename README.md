# MarkDownBlog

## Quick start with Django

1. Add "dmdb" to your `INSTALLED_APPS`

2. Include the MarkDownBlog URLconf in your `urls.py`:
    url(r'^blog/', include('dmdb.urls')),

    or even

    url(r'', include('dmdb.urls')),

3. Run `python manage.py migrate` to create the models
4. create the `dbmdb` folder, where each file is a post (whose slug is the filename):

    title: New Blog!
    date: 2015-12-24
    is_visible: 1
    author: myself
    sites: myself.com

    Hey guys ! I got a new blog \o/

    I can even write code in it !

        #!python

        if code.written:
            code.color()

5. Run `python manage.py update_blog` to update your database
6. Run `python runserver` and checkout http://127.0.0.1:8000
