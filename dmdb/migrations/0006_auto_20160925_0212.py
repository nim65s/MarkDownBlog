# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-09-25 00:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dmdb', '0005_tags_categories'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogcategory',
            options={'ordering': ['title'], 'verbose_name': 'Catégorie'},
        ),
        migrations.AlterModelOptions(
            name='blogtag',
            options={'ordering': ['title'], 'verbose_name': 'Tag'},
        ),
    ]
