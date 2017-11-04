from django.contrib import admin
from django.forms import ValidationError
from django.forms.models import BaseInlineFormSet
from django.utils import timezone
from .models import Prediction, PredOption, notify_pred_load
from question.models import Category
from django.contrib import messages


class PredOptionInlineFormSet(BaseInlineFormSet):

    def clean(self):
        super(PredOptionInlineFormSet, self).clean()
        initial_num = len(list(filter(lambda f: not self._should_delete_form(f), self.initial_forms)))
        extra_num = len(list(filter(lambda f: f.has_changed() and not self._should_delete_form(f), self.extra_forms)))
        if initial_num + extra_num < 2:
            raise ValidationError('There has to be at least 2 options')
        if initial_num == 0:
            for field in self.forms:
                if 'is_correct' in field.cleaned_data and field.cleaned_data['is_correct']:
                    raise ValidationError('You cant add correct '
                                          'answers on insert')
        else:
            total = 0
            for field in self.forms:
                if not field.is_valid() or not ('is_correct' in field.cleaned_data):
                    continue
                if field.cleaned_data['is_correct'] and not (self._should_delete_form(field)):
                    total += 1
            if total == 1 :
                notify_pred_load(self.instance.id)
            elif total > 1:
                raise ValidationError('You entered ' + str(total) +
                                      ' correct answers. '
                                      'There can only be 1 or 0')


class PredOptionInline(admin.TabularInline):
    model = PredOption
    formset = PredOptionInlineFormSet
    extra = 2

    def has_delete_permission(self, request, obj=None):
        return False

    def get_extra(self, request, obj=None, **kwargs):
        extra = 2
        if obj:
            amount_options = PredOption.objects.filter(prediction=obj)
            self.max_num = len(amount_options)
        return extra


class PredictionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['description', 'category',
                           'finish_bet_date', 'finish_pred']}),
    ]
    inlines = [PredOptionInline]


admin.site.register(Prediction, PredictionAdmin)
