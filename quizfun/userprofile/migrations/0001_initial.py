# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-10 23:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import userprofile.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hobbies', models.TextField(blank=True, null=True)),
                ('favorites_categories', models.CharField(blank=True, max_length=200, null=True)),
                ('coins', models.IntegerField(default=0)),
                ('avatar', models.FileField(blank=True, null=True, upload_to='useravatars')),
                ('prediction_lost_am', models.IntegerField(default=0)),
                ('prediction_win_am', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
