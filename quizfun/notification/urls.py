from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    url(r'notification', views.list_notification, name='list_notification'),

]
