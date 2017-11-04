from django.db import models
from question.models import Category
from userprofile.models import UserProfile
from django.forms import ValidationError
import datetime
from django.utils import timezone


class Prediction(models.Model):
    description = models.CharField(max_length=200)
    category = models.ForeignKey(Category)
    date_started = models.DateTimeField(auto_now_add=True,blank=False)
    finish_bet_date = models.DateTimeField(blank=False)
    finish_pred = models.DateTimeField(blank=False)

    def __str__(self):
        return self.description


class PredOption(models.Model):
    prediction = models.ForeignKey(Prediction)
    description = models.CharField(max_length=200)
    probability = models.DecimalField(max_digits=4, decimal_places=2,
                                      default=1.00)
    is_correct = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.description

    def clean(self):
        if self.probability <= 1.00:
            raise ValidationError('Put a positive and significant probability')
        if self.prediction:
            if self.prediction.finish_pred > timezone.now() and self.is_correct:
                raise ValidationError('You cant upload the correct answer yet')


class OptionBet(models.Model):
    userprofile = models.ForeignKey(UserProfile)
    optionbet = models.ForeignKey(PredOption)
    amount_bet = models.IntegerField()


def notify_pred_load(id_prediction):
    from notification.models import Notification
    from prediction.models import Prediction, PredOption, OptionBet
    tupla_options = PredOption.objects.filter(prediction=id_prediction)
    for op in tupla_options:
        tupla_users_optbet = OptionBet.objects.filter(optionbet=op)
        for us in tupla_users_optbet:
            if op.is_correct:
                us.userprofile.add_coins(op.probability * us.amount_bet)
                n = Notification(description='Response to ' + op.description +
                                 ' has already been loaded, you won '
                                 + str(op.probability * us.amount_bet)
                                 + ' coins!', profile=us.userprofile)
                n.save()
            else:
                n = Notification(description='Response to ' + op.description +
                                 ' has already been loaded, you lost ' +
                                 str(us.amount_bet) + ' coins!',
                                 profile=us.userprofile)
                n.save()
