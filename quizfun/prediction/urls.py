from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views
#from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'prediction', views.prediction, name='prediction'),
    url(r'^bet/(?P<prediction_id>\d+)/$', views.bet, name='bet'),
    url(r'^save_bet', views.save_bet, name='save_bet'),
    url(r'^my_bets', views.my_bets, name='my_bets'),
]
