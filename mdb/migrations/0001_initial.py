# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.manager
import datetime
import django.contrib.sites.shortcuts
import django.contrib.sites.managers


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogEntry',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('slug', models.CharField(max_length=200, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('date', models.DateField(default=datetime.date.today)),
                ('is_visible', models.BooleanField(default=True)),
                ('content', models.TextField()),
                ('author', models.CharField(max_length=100)),
                ('template', models.CharField(default='post', max_length=50)),
                ('sites', models.ManyToManyField(default=django.contrib.sites.shortcuts.get_current_site, to='sites.Site')),
            ],
            managers=[
                ('objects', django.db.models.manager.Manager()),
                ('on_site', django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
    ]
