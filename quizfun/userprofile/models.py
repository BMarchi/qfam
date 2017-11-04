# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import os


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='userprofile',
                                on_delete=models.CASCADE)
    hobbies = models.TextField(null=True, blank=True)
    favorites_categories = models.CharField(null=True,
                                            max_length=200,
                                            blank=True)
    coins = models.IntegerField(null=True, default=50)
    avatar = models.FileField(null=True,
                              upload_to='useravatars',
                              blank=True)
    prediction_lost_am = models.IntegerField(null=True, default=0)
    prediction_win_am = models.IntegerField(null=True, default=0)
    bday = models.DateField(auto_now=False, auto_now_add=False,
                            null=True)
    balance = models.IntegerField(default=0)

    def amount_notifications(self):
        return len(Notification.objects.filter(profile=self.user.id,
                                               viewed=False))

    def add_coins(self, coins):
        self.coins += coins
        self.balance += coins
        self.save()

    def sub_coins(self, coins):
        if coins > self.coins:
            self.balance -= self.coins
            self.coins = 0
        else:
            self.balance -= coins
            self.coins -= coins
        self.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


from notification.models import Notification
