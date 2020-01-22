from django.db import models

class DefaultUser(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, null=True)

    email = models.EmailField(unique=True, null=False, blank=False)
    username = models.CharField(max_length=50, unique=True, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)
    
    postalcode = models.CharField(max_length=30, blank=True, null=True)
    address_line = models.CharField(max_length=120, blank=True, null=True)
    address_complement = models.CharField(max_length=120, blank=True, null=True)
    city = models.CharField(max_length=50,blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    
    avatar = models.URLField(blank=True, null=True)
    biography = models.CharField(max_length=200,null=True, blank=True)
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

class ForgotPassword(models.Model):
    user = models.OneToOneField(DefaultUser, on_delete=models.CASCADE, primary_key=True)
    token = models.CharField(max_length=200)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)