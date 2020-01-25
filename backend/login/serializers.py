from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import DefaultUser, ForgotPassword

class DefaultUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = DefaultUser
        fields = ['id','first_name', 'last_name', 'phone', 'email','username','password',
        'postalcode','address_line','address_complement','state','country','avatar',
        'date_of_birth','biography','date_joined', 'updated_date', 'validated_email']

        read_only_fields = ['date_joined','updated_date', 'validated_email']

        extra_kwargs = {'password': {'write_only': True}}

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class RecoverPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
    new_password = serializers.CharField()

class SessionSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()