# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-14 14:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0006_userprofile_bday'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='bday',
            field=models.DateField(null=True),
        ),
    ]
