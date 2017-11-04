# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Question, Answer, Solved, QuestionStarted
from userprofile.models import UserProfile
import random
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from datetime import datetime
from django.utils import timezone
from notification.models import Notification
from django.contrib.auth.decorators import user_passes_test

def admin_check(user):
    return (not user.is_superuser)

@user_passes_test(admin_check,login_url='/',redirect_field_name=None)
@login_required(login_url='/login')
def get_question(request):
    usuario = request.user
    started_question = QuestionStarted.objects.filter(user=usuario)
    if started_question:
        started_question = started_question[0]
        time_re = started_question.remaining_time()
        if time_re > 0:
            context = {'pregunta': started_question.question,
                       'time_left': time_re}
            return render(request, 'get_question.html', context)
        else:
            usuario.userprofile.sub_coins(started_question.question.loss_coins)
            a = Notification(description=('Remember not to close '
                                          'the question-mode window '
                                          'while you\'re playing. '
                                          'You have been discounted '
                                          '%s coins.'
                                          % started_question.question.loss_coins),
                             profile=usuario.userprofile)
            a.save()
            started_question.delete()
    coins = usuario.userprofile.coins
    if (coins < 10):
        messages.error(request, 'You don\'t have enough coins :(')
        return redirect('index')
    all_solut = Solved.objects.filter(user=usuario)
    solv_quest = []
    for s in all_solut:
        solv_quest.append(s.question)
    all_quest = Question.objects.all()
    unsolved = set(all_quest) - set(solv_quest)
    try:
        question = random.choice(list(unsolved))
    except IndexError:
        messages.error(request, 'No new questions avalaible :(')
        return redirect('index')
    context = {'pregunta': question,
               'time_left': question.time_limit}
    QuestionStarted.objects.create(question=question, user=usuario)
    return render(request, 'get_question.html', context=context)

@user_passes_test(admin_check,login_url='/',redirect_field_name=None)
@login_required(login_url='/login')
def check_answer(request):
    if request.method == 'POST':
        usuario = request.user
        profile = usuario.userprofile
        try:
            resp = Answer.objects.get(pk=request.POST['answer'])
            QuestionStarted.objects.filter(user=usuario)[0].delete()
            q = resp.question
            data = {
                'resp': resp.is_correct
            }
            if resp.is_correct:
                profile.add_coins(q.reward_coins)
                s = Solved(user=usuario, question=q)
                s.save()
            else:
                profile.sub_coins(q.loss_coins)
        except (MultiValueDictKeyError, IndexError) as e:
            q = QuestionStarted.objects.filter(user=usuario)[0]
            profile.sub_coins(q.question.loss_coins)
            q.delete()
            data = {'vacio': True}
        return JsonResponse(data)
    return redirect('index')
