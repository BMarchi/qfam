# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-11 18:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0002_userprofile_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='coins',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='prediction_lost_am',
            field=models.IntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='prediction_win_am',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
