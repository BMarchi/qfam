# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.

from userprofile.models import UserProfile
from .models import Category, Difficulty, Answer, Question, Solved
from django.test import Client


def create_category(category_name):
    return Category.objects.create(category_name=category_name)


def create_difficulty(difficulty, max_reward, min_reward, max_loss, min_loss):
    return Difficulty.objects.create(difficulty=difficulty,
                                     max_reward=max_reward,
                                     min_reward=min_reward,
                                     max_loss=max_loss,
                                     min_loss=min_loss)


def create_answer(question, description, is_correct):
    return Answer.objects.create(question=question,
                                 description=description,
                                 is_correct=is_correct)


def create_question(description, category, difficulty, reward_coins, loss_coins):
    return Question.objects.create(description=description, category=category,
                                   difficulty=difficulty,
                                   reward_coins=reward_coins,
                                   loss_coins=loss_coins)


class QuestionTestCase(TestCase):

    def test_create_question(self):
        c = create_category('Arte')
        d = create_difficulty('Media', 5, 1, 5, 1)
        q = create_question('Funciona?', c, d, 5, 5)
        a_1 = create_answer(q, 'Si', True)
        a_2 = create_answer(q, 'No', False)
        pregunta = Question.objects.all()[0]
        self.assertEqual(pregunta, q)

    def test_correct_answer(self):
        client = Client()
        datos = {
          'username': 'us_1',
          'password1': 'casa1234',
          'password2': 'casa1234',
          'email': 'usuario1@gmail.com',
          'hobbies': 'Testear',
          'first_name': 'Juan',
          'last_name': 'Perez',
          'birthdate': '2017-08-01'
          }
        response = client.post('/register_user', datos)

        c = create_category('Arte')
        d = create_difficulty('Media', 5, 1, 5, 1)
        q = create_question('Funciona?', c, d, 5, 5)
        a_1 = create_answer(q, 'Si', True)
        a_2 = create_answer(q, 'No', False)

        datos = {'answer': 1}

        response = client.get('/get_question')
        response = client.post('/check_answer', datos)
        # Correct Answer

        coins = UserProfile.objects.all()[0].coins
        self.assertEqual(coins, 55)
        solved = len(Solved.objects.all())
        self.assertEqual(solved, 1)

    def test_incorrect_answer(self):
        client = Client()
        datos = {
          'username': 'us_1',
          'password1': 'casa1234',
          'password2': 'casa1234',
          'email': 'usuario1@gmail.com',
          'hobbies': 'Testear',
          'first_name': 'Juan',
          'last_name': 'Perez',
          'birthdate': '2017-08-01'
          }
        response = client.post('/register_user', datos)

        c = create_category('Arte')
        d = create_difficulty('Media', 5, 1, 5, 1)
        q = create_question('Funciona?', c, d, 5, 5)
        a_1 = create_answer(q, 'Si', True)
        a_2 = create_answer(q, 'No', False)

        datos = {'answer': 2}

        response = client.get('/get_question')
        response = client.post('/check_answer', datos)
        # Incorrect Answer

        coins = UserProfile.objects.all()[0].coins
        self.assertEqual(coins, 45)
        solved = len(Solved.objects.all())
        self.assertEqual(solved, 0)

    def test_leave_and_correct_answer(self):
        client = Client()
        datos = {
          'username': 'us_1',
          'password1': 'casa1234',
          'password2': 'casa1234',
          'email': 'usuario1@gmail.com',
          'hobbies': 'Testear',
          'first_name': 'Juan',
          'last_name': 'Perez',
          'birthdate': '2017-08-01'
          }
        response = client.post('/register_user', datos)

        c = create_category('Arte')
        d = create_difficulty('Media', 5, 1, 5, 1)
        q = create_question('Funciona?', c, d, 5, 5)
        a_1 = create_answer(q, 'Si', True)
        a_2 = create_answer(q, 'No', False)

        response = client.get('/get_question')
        response = client.get('/get_question')
        response = client.get('/get_question')
        # I forgot to answer
        datos = {'answer': 1}
        response = client.post('/check_answer', datos)

        coins = UserProfile.objects.all()[0].coins
        self.assertEqual(coins, 55)
        solved = len(Solved.objects.all())
        self.assertEqual(solved, 1)

    def test_leave_and_incorrect_answer(self):
        client = Client()
        datos = {
          'username': 'us_1',
          'password1': 'casa1234',
          'password2': 'casa1234',
          'email': 'usuario1@gmail.com',
          'hobbies': 'Testear',
          'first_name': 'Juan',
          'last_name': 'Perez',
          'birthdate': '2017-08-01'
          }
        response = client.post('/register_user', datos)

        c = create_category('Arte')
        d = create_difficulty('Media', 5, 1, 5, 1)
        q = create_question('Funciona?', c, d, 5, 5)
        a_1 = create_answer(q, 'Si', True)
        a_2 = create_answer(q, 'No', False)

        response = client.get('/get_question')
        response = client.get('/get_question')
        response = client.get('/get_question')
        # I forgot to answer
        datos = {'answer': 2}
        response = client.post('/check_answer', datos)

        coins = UserProfile.objects.all()[0].coins
        self.assertEqual(coins, 45)
        solved = len(Solved.objects.all())
        self.assertEqual(solved, 0)

    def test_no_money(self):
        client = Client()
        datos = {
          'username': 'us_1',
          'password1': 'casa1234',
          'password2': 'casa1234',
          'email': 'usuario1@gmail.com',
          'hobbies': 'Testear',
          'first_name': 'Juan',
          'last_name': 'Perez',
          'birthdate': '2017-08-01'
          }
        response = client.post('/register_user', datos)

        perfil = UserProfile.objects.all()[0]
        perfil.coins = 5
        perfil.save()

        coins = UserProfile.objects.all()[0].coins
        self.assertEqual(coins, 5)

        c = create_category('Arte')
        d = create_difficulty('Media', 5, 1, 5, 1)
        q = create_question('Funciona?', c, d, 5, 5)
        a_1 = create_answer(q, 'Si', True)
        a_2 = create_answer(q, 'No', False)

        response = client.get('/get_question')
        # I dont have money

        coins = UserProfile.objects.all()[0].coins
        self.assertEqual(coins, 5)
        self.assertEqual(response.status_code, 302)
