# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from userprofile.models import UserProfile

def global_ranking(request):
    ranking = UserProfile.objects.all().order_by('-coins')
    rank_list = []
    for x in ranking:
    	if not x.user.is_superuser:
    		rank_list.append(x)
    context = {'ranking': rank_list}
    return render(request, 'ranking.html', context=context)

def monthly_ranking(request):
	ranking = UserProfile.objects.all().order_by('-balance')
	rank_list = []
	for x in ranking:
		if not x.user.is_superuser:
			rank_list.append(x)
		context = {'ranking': rank_list}
	return render(request, 'monthly_ranking.html', context=context)