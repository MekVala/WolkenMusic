# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2018-03-18 06:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_playlist_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='played_counter',
            field=models.IntegerField(default=0),
        ),
    ]
