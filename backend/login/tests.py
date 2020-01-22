from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from collections import OrderedDict
import json

class LoginTest(APITestCase):
    client = APIClient()
    user_data = {   "username": "Teste",
                    "password": "teste321",
                    "email": "teste@gmasi.com",
                    "avatar": "https://none.com/"    }
