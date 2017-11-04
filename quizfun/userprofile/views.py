# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .models import UserProfile
from .forms import ProfileForm
from .forms import EditForm

from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

def admin_check(user):
    return (not user.is_superuser)

def register_user(request):
    args = {}
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST or None, request.FILES)
        if profile_form.is_valid():
            user = profile_form.save()
            user.refresh_from_db()
            user.userprofile.avatar = profile_form.cleaned_data['avatar']
            user.userprofile.hobbies = profile_form.cleaned_data['hobbies']
            user.userprofile.favorites_categories = profile_form.cleaned_data['favorites_categories']
            user.userprofile.bday = profile_form.cleaned_data['birthdate']
            user.save()
            login(request, user)
            return redirect('index')
    else:
        profile_form = ProfileForm()
    args['form'] = profile_form
    return render(request, 'register.html',
                  {'profile_form': profile_form}, args)

@user_passes_test(admin_check,login_url='/',redirect_field_name=None)
@login_required(login_url='/login')
def profile_user(request):
    usuario = request.user
    data = {'hobbies': usuario.userprofile.hobbies,
            'coins': usuario.userprofile.coins,
            'first_name': usuario.first_name,
            'last_name': usuario.last_name,
            'fav_categories': usuario.userprofile.favorites_categories,
            'pred_right': usuario.userprofile.prediction_win_am,
            'pred_lost': usuario.userprofile.prediction_lost_am,
            'email': usuario.email,
            'bday': usuario.userprofile.bday,
            }
    return render(request, 'profile.html', context=data)

@user_passes_test(admin_check,login_url='/',redirect_field_name=None)
@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user or None, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request,
                             'Your password was successfully updated!')
            return redirect('index')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

@user_passes_test(admin_check,login_url='/',redirect_field_name=None)
@login_required(login_url='/login')
def edit_profile(request):
    user = request.user
    profile = user.userprofile

    # Process the form data
    if request.method == 'POST':
        # Create a form instance
        form = EditForm(request.POST, request.FILES)
        if form.is_valid():
            profile.hobbies = form.cleaned_data['hobbies']
            profile.favorites_categories = form.cleaned_data['favorites_categories']
            profile.bday = form.cleaned_data['birthdate']
            if request.FILES.get('avatar') is not None:
                user.userprofile.avatar = form.cleaned_data['avatar']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            profile.save()
            user.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('index')

    # if a GET (or any other method) we'll create a blank form
    else:
        try:
            lista = profile.favorites_categories.split(",")
        except AttributeError:
            lista = []
        data = {'first_name': user.first_name,
                'last_name': user.last_name,
                'hobbies': profile.hobbies,
                'favorites_categories': lista,
                'birthdate': profile.bday,
                'email': user.email
                }
        form = EditForm(initial=data)

    return render(request, 'edit_profile.html', {'form': form})
