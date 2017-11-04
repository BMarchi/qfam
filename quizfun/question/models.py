# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone
# Create your models here.


class Category(models.Model):
    category_name = models.CharField(max_length=60, unique=True)

    def __str__(self):
        return self.category_name


class Difficulty(models.Model):
    difficulty = models.CharField(max_length=60, unique=True)

    max_reward = models.IntegerField(default=0)
    min_reward = models.IntegerField(default=0)
    max_loss = models.IntegerField(default=0)
    min_loss = models.IntegerField(default=0)

    def __str__(self):
        return self.difficulty


class Question(models.Model):
    description = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(Category)
    reward_coins = models.IntegerField(default=0)
    loss_coins = models.IntegerField(default=0)
    difficulty = models.ForeignKey(Difficulty)
    time_limit = models.IntegerField(default=5)

    def __str__(self):
        return self.description

    def clean(self):
        super(Question, self).clean_fields()
        max_reward = self.difficulty.max_reward
        min_reward = self.difficulty.min_reward

        max_loss = self.difficulty.max_loss
        min_loss = self.difficulty.min_loss

        if (self.reward_coins < min_reward) or (self.reward_coins >
                                                max_reward):
            raise ValidationError('Invalid coins! Remember '
                                  'that the acceptable range '
                                  'of the award is: '
                                  + str(max_reward) + ' - ' + str(min_reward))
        elif (self.loss_coins < min_loss) or (self.loss_coins > max_loss):
            raise ValidationError('Invalid coins! Remember '
                                  'that the acceptable range '
                                  'the loss is :' + str(max_loss) +
                                  ' - ' + str(min_loss))
        elif (self.time_limit < 5):
            raise ValidationError('Invalid time limit! remember '
                                  'that time must be greater than '
                                  'or equal to 5')


class Answer(models.Model):
    question = models.ForeignKey(Question)
    description = models.CharField(max_length=200)
    is_correct = models.BooleanField()

    def __str__(self):
        return self.description


class Solved(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)


class QuestionStarted(models.Model):
    user = models.ForeignKey(User)
    question = models.ForeignKey(Question)
    updated = models.DateTimeField(auto_now_add=True)

    def remaining_time(self):
        time = self.question.time_limit
        time_now = datetime.now(timezone.utc)
        return time - int((time_now - self.updated).total_seconds())
