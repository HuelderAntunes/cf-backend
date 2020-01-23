from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import DefaultUser, ForgotPassword

class DefaultUserSerializer(serializers.ModelSerializer):
    class Meta():
        model = DefaultUser
        fields = ['first_name', 'last_name', 'phone', 'email','username','password',
        'postalcode','address_line','address_complement','state','country','avatar',
        'biography','date_joined', 'updated_date']

        read_only_fields = ['date_joined','updated_date']

        extra_kwargs = {'password': {'write_only': True}}

class SessionSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()