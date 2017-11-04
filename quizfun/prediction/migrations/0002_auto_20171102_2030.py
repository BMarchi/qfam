# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 20:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prediction',
            name='date_started',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='prediction',
            name='finish_bet_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='prediction',
            name='finish_pred',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='predoption',
            name='probability',
            field=models.DecimalField(decimal_places=2, default=1.0, max_digits=4),
        ),
    ]