# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from .models import Notification
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

def admin_check(user):
    return (not user.is_superuser)

@user_passes_test(admin_check,login_url='/',redirect_field_name=None)
@login_required(login_url='/login')
def list_notification(request):
    user = request.user
    n = Notification.objects.filter(profile=user.userprofile).order_by('-time')
    listav = []
    listanv = []
    for x in n:
        if x.viewed:
                listav.append(x)
        else:
                listanv.append(x)
        x.viewed = True
        x.save()
        listav = listav[0:10]
    return render(request, 'list_notification.html', {'vistos': listav,
                                                      'no_vistos': listanv})
