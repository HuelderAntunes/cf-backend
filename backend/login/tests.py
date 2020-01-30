from django.test import TestCase
from .models import ForgotPassword
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from collections import OrderedDict
import bcrypt
import json


class LoginTest(APITestCase):
    user_data = {
        'username': 'test',
                    'password': '123',
                    'email': 'teste@gmail.com',
                    'avatar': 'https://none.com/',
                    'first_name': 'Test',
                    'last_name': 'Name',
                    'postalcode': '0555368454',
                    'phone': '5519996285379',
                    'address_line': 'Av. test address, Paulinia',
                    'address_complement': 'Interesting complement',
                    'state': 'SP',
                    'country': 'BRAZIL',
                    'date_of_birth': '2001-02-10',
                    'avatar': 'https://none.com/',
                    'biography': 'I\' just a test profile.'
    }

    def test_register(self):
        client = APIClient()
        response = client.post('/users/', self.user_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['email'], self.user_data['email'])

    def test_sessions(self):
        client = APIClient()
        client.post('/users/', self.user_data, format='json')

        response = self.client.post('/sessions/',
                                    {
                                        'username': self.user_data['username'],
                                        'password': self.user_data['password']
                                    },
                                    format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_retrieve_edit_profile(self):
        client = APIClient()
        user = client.post('/users/', self.user_data, format='json')

        user_id = user.data['id']

        session = client.post('/sessions/',
                              {
                                  'username': self.user_data['username'],
                                  'password': self.user_data['password']
                              },
                              format='json')

        token = session.data['access']

        retrieve_err = client.get('/users/')
        self.assertEqual(retrieve_err.status_code,
                         status.HTTP_401_UNAUTHORIZED)

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        retrieve_all = client.get('/users/')
        self.assertEqual(retrieve_all.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_all.data['id'], user_id)

        retrieve_pk = client.get('/users/%i/' % user_id)
        self.assertEqual(retrieve_pk.status_code, status.HTTP_200_OK)
        self.assertEqual(retrieve_pk.data['id'], user_id)

        retrieve_other = client.get('/users/50/')
        self.assertEqual(retrieve_other.status_code,
                         status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', retrieve_other.data)

        edit_name = client.patch('/users/%i/' % user_id, {
            'first_name': 'Testfirst'
        })
        self.assertEqual(edit_name.status_code, status.HTTP_200_OK)
        self.assertIn(edit_name.data['first_name'], 'Testfirst')

    def test_recover_password(self):
        client = APIClient()
        user = client.post('/users/', self.user_data, format='json')

        client.post('/forgotpassword/',
                    {
                        'email': self.user_data['email']
                    },
                    format='json')

        forgot_pass = ForgotPassword.objects.get(user=user.data['id'])

        self.assertIsNotNone(forgot_pass)
        self.assertIsNotNone(forgot_pass.token)

        recover_token = str(bcrypt.hashpw(b'123', bcrypt.gensalt()), 'utf-8')

        forgot_pass.token = recover_token
        forgot_pass.save()

        recover_err = client.post('/forgotpassword/recover/',
                                  {
                                      'email': self.user_data['email'],
                                      'new_password': 'test',
                                      'token': '45654'
                                  },
                                  format='json')

        self.assertIn('error', recover_err.data)

        recover = client.post('/forgotpassword/recover/',
                              {
                                  'email': self.user_data['email'],
                                  'new_password': 'test',
                                  'token': '123'
                              },
                              format='json')

        self.assertIn('success', recover.data)
