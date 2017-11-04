# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from userprofile.models import UserProfile
from django.utils import timezone


class Notification(models.Model):
    description = models.CharField(max_length=200)
    time = models.DateTimeField(default=timezone.now)
    profile = models.ForeignKey(UserProfile, related_name='notificaciones')
    viewed = models.BooleanField(default=False)

    def __str__(self):
        return self.description
