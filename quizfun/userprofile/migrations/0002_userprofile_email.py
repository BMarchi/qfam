# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-10 23:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(blank=True, max_length=100, unique=True),
        ),
    ]
