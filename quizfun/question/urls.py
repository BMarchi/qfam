from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    url(r'^get_question', views.get_question, name="get_question"),
    url(r'^check_answer', views.check_answer, name="check_answer"),
]
