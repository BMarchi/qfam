# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib import admin
from django.forms.models import BaseInlineFormSet
from django.forms import ValidationError
from .models import Category, Difficulty, Answer, Question


class AnswerInlineFormSet(BaseInlineFormSet):

    def clean(self):
        super(AnswerInlineFormSet, self).clean()
        initial_num = len(list(filter(lambda f: not self._should_delete_form(f), self.initial_forms)))
        extra_num = len(list(filter(lambda f: f.has_changed() and not self._should_delete_form(f), self.extra_forms)))
        if initial_num + extra_num < 2:
            raise ValidationError("There has to be at least 2 answers")
        total = 0
        for field in self.forms:
            if not field.is_valid() or not ('is_correct'
                                            in field.cleaned_data):
                continue
            if field.cleaned_data['is_correct'] and not (self._should_delete_form(field)):
                total += 1
        if total != 1:
            raise ValidationError('You entered ' + str(total) +
                                  ' correct answers. There can only be 1')


class AnswerInline(admin.TabularInline):
    model = Answer
    formset = AnswerInlineFormSet
    extra = 2


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['description',
                                         'category', 'difficulty']}),
        ('Coins', {'fields': ['reward_coins', 'loss_coins']}),
        ('Time', {'fields': ['time_limit']}),
    ]
    inlines = [AnswerInline]
    list_display = ('description', 'category',
                    'difficulty', 'reward_coins',
                    'loss_coins', 'time_limit')


class DifficultyAdmin(admin.ModelAdmin):
    list_display = ('difficulty', 'max_reward',
                    'min_reward', 'max_loss', 'min_loss')


admin.site.register(Question, QuestionAdmin)
admin.site.register(Category)
