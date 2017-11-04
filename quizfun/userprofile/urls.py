from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'register_user', views.register_user, name='register_user'),
    url(r'profile_user', views.profile_user, name='profile_user'),
    url(r'^login/$', auth_views.login,
        {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout,
        {'next_page': 'index'}, name='logout'),
    url(r'^change_password$', views.change_password, name='change_password'),
    url(r'^edit_profile$', views.edit_profile, name='edit_profile'),
]
