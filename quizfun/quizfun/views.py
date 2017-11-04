from django.http import HttpResponse
from django.shortcuts import render
from userprofile.models import UserProfile


def index(request):
    return render(request, 'index.html')
