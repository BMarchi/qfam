# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.

from userprofile.models import UserProfile
from .models import Notification
from django.test import Client

def create_notification(description, profile):
    return Notification.objects.create(description=description, profile=profile)


class NotificationTestCase(TestCase):

    def test_retrieve_notification(self):
        c = Client()
        datos = {
          'username' : 'us_1',
          'password1' : 'casa1234',
          'password2' : 'casa1234',
          'email' : 'usuario1@gmail.com',
          'hobbies' : 'Testear',
          'first_name' : 'Juan',
          'last_name' : 'Perez',
          'birthdate' : '2017-08-01'
          }
        response = c.post('/register_user', datos)
        perfil = UserProfile.objects.all()[0]
        create_notification('Prueba_1', perfil)
        create_notification('Prueba_2', perfil)
        # Hay nuevas notificaciones
        no_vistos = len(Notification.objects.filter(viewed=False))
        self.assertEqual(no_vistos, 2)
        response = c.get('/list_notification')
        # No hay nuevas notificaciones
        no_vistos = len(Notification.objects.filter(viewed=False))
        self.assertEqual(no_vistos, 0)
