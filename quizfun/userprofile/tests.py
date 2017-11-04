# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase

from .models import UserProfile

from django.test import Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import auth

def create_user(username, password, email):
    return User.objects.create(username=username, password=password, email=email)

class UserProfileTestCase(TestCase):

    # Set 1
    def test_index_is_home_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_working_login(self):
        usuario1 = create_user('us_1', 'casa1234', 'usuario1@gmail.com')
        c = Client()
        response = c.post('/login/', {'username': 'us_1', 'password': 'casa1234'})
        self.assertEqual(response.status_code, 200)
    
    def test_working_registration(self):
        c = Client()
        datos = {
          'username' : 'us_1',
          'password1' : 'casa1234',
          'password2' : 'casa1234',
          'email' : 'usuario1@gmail.com',
          'hobbies' : 'testear',
          'first_name' : 'Juan',
          'last_name' : 'Perez',
          'birthdate' : '2017-08-01',
          }

        response = c.post('/register_user', datos)
        perfil = UserProfile.objects.all()[0]
        usuario = User.objects.all()[0]
        self.assertEqual(perfil.hobbies, 'testear')
        self.assertEqual(usuario.first_name, 'Juan')

    def test_registration_with_same_email(self):
        c_1 = Client()
        datos_1 = {
          'username' : 'us_1',
          'password1' : 'casa1234',
          'password2' : 'casa1234',
          'email' : 'usuario1@gmail.com',
          'hobbies' : 'Testear',
          'first_name' : 'Juan',
          'last_name' : 'Perez',
          'birthdate' : '2017-08-01'
          }

        c_2 = Client()
        datos_2 = {
          'username' : 'us_2',
          'password1' : 'casa1234',
          'password2' : 'casa1234',
          'email' : 'usuario1@gmail.com',
          'hobbies' : 'Romper',
          'first_name' : 'Pedro',
          'last_name' : 'Jobs',
          'birthdate' : '2017-09-01'
          }

        response_1 = c_1.post('/register_user', datos_1)
        response_2 = c_2.post('/register_user', datos_2)
        cant = len(UserProfile.objects.all())
        self.assertEqual(cant, 1)

    def test_logout(self):
        usuario = create_user('lala', 'lala1234', 'lalita@gmail.com')
        c = Client()
        response = c.post('/login/', {'username': 'lala', 'password': 'lala1234'})
        response = c.post('/logout/', follow=True)

        user = auth.get_user(self.client)

        self.assertEqual(response.status_code, 200)
        self.assertFalse(user.is_authenticated())
        self.assertTrue(b'login' in response.content)

    def test_visit_profile_after_registration(self):
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
        response = c.post('/profile_user')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')


    # Set 2
    def test_get_register_html(self):
        response = self.client.get('/register_user', follow=True)
        self.assertTemplateUsed(response, 'register.html')

    def test_create_account(self):
        form_data = {'username': 'jorge123',
                     'email': 'jorge@hotmail.com',
                     'password1': 'carlos123',
                     'password2': 'carlos123',}
        response = self.client.post('/register_user', form_data)
        self.assertEqual(response.status_code, 200)

    def test_left_password_empty(self):
        form_data = {'username': 'tevez123',
                     'email': 'ejem@ho.com',}
        response = self.client.post('/register_user', form_data)
        self.assertFormError(response, 'profile_form','password1', "This field is required.")

    def test_short_password_and_confmismatch(self):
        form_data = {'username': 'tevez123',
                     'email': 'ejem@ho.com',
                     'password1': 'asd',
                     'password2': 'asd',}
        response = self.client.post('/register_user', form_data)
        self.assertFormError(response, 'profile_form','password2', "This password is too short. It must contain at least 8 characters.")
        form_data = {'username': 'tevez123',
                     'email': 'ejem@ho.com',
                     'password1': 'carlito123',
                     'password2': 'carlito122',}
        response = self.client.post('/register_user', form_data)
        self.assertFormError(response, 'profile_form','password2', "The two password fields didn't match.") 

