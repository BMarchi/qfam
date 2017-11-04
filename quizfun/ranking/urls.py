from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    url(r'^ranking', views.global_ranking, name="ranking"),
    url(r'^monthly_ranking', views.monthly_ranking, name="monthly_ranking"),
]