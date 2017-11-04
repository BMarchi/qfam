from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Prediction, PredOption, OptionBet
from datetime import datetime
from django.utils import timezone
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

def admin_check(user):
    return (not user.is_superuser)

@user_passes_test(admin_check,login_url='/',redirect_field_name=None)
@login_required(login_url='/login')
def prediction(request):
    profile = request.user.userprofile
    if (profile.coins >= 1):
        p = Prediction.objects.filter(finish_bet_date__gte=datetime.now(timezone.utc))
        p_list = []
        for x in p:
            p_list.append(x)
        my_bets = OptionBet.objects.filter(userprofile=profile)
        bet_list = []
        for b in my_bets:
            bet_list.append(b.optionbet.prediction)
        pred = set(p_list) - set(bet_list)
        return render(request, "prediction.html",{'predictions': pred})
    else:
        messages.error(request, 'You don\'t have enough coins :(')
        return redirect('index')

@user_passes_test(admin_check,login_url='/',redirect_field_name=None)
@login_required(login_url='/login')
def bet(request, prediction_id):
    p = get_object_or_404(Prediction,pk=prediction_id)
    if (p.finish_bet_date > datetime.now(timezone.utc)):
        p_options = PredOption.objects.filter(prediction = prediction_id)
        p_options_list = []
        for x in p_options:
            p_options_list.append(x)
        return render(request, 'bet.html', {'prediction': p, 'p_options_list': p_options_list})
    else:
        messages.error(request, 'This prediction has alredy expired')
        return redirect('index')

@user_passes_test(admin_check,login_url='/',redirect_field_name=None)
@login_required(login_url='/login')
def save_bet(request):
    if request.POST:
        profile = request.user.userprofile
        selected_option = PredOption.objects.get(pk=request.POST['selected'])
        amount_bet = int(request.POST['bet'])
        option = OptionBet(userprofile=profile,optionbet=selected_option,amount_bet=amount_bet)
        option.save()
        profile.sub_coins(amount_bet)
        data = {
            'status' : True
        }
        messages.success(request, 'Your bet has been saved. Your coins will be detain :)')
    return redirect('index')

@user_passes_test(admin_check,login_url='/',redirect_field_name=None)
@login_required(login_url='/login')
def my_bets(request):
    profile = request.user.userprofile
    my_bets = OptionBet.objects.filter(userprofile = profile)
    context = {'my_bets': my_bets}
    return render(request, 'my_bets.html', context)
