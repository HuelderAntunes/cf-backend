from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from collections import OrderedDict

class LoginTest(APITestCase):
    client = APIClient()
    user_data = {   "username": "Teste",
                        "password": "teste321",
                        "email": "teste@gmasi.com",
                        "groups": []    }

    def test_user(self):
        response = self.client.post('/user/', self.user_data, format='json')
        self.assertEqual(response.data,
                        self.user_data, "Be able to create user")

        response = self.client.get('/user/1/', format='json')
        self.assertEqual(response.data, self.user_data,
                        "Be able to get an user")

        put_data = {"email": "teste@gmail.com"}
        response = self.client.put('/user/1/', self.user_data, format='json')
        self.assertEqual(response.data, self.user_data,
                        "Be able to edit an user")

        response = self.client.get('/user/', format='json')
        self.assertEqual(response.data.count, 1,
                        "Be able to get all users")

