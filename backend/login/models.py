from django.db import models
from django.contrib.auth.models import AbstractUser, Group

class DefaultUser(AbstractUser):
    phone = models.CharField(max_length=15, blank=True, null=True)

    password = models.CharField(max_length=100, null=False, blank=False)

    postalcode = models.CharField(max_length=30, blank=True, null=True)
    address_line = models.CharField(max_length=120, blank=True, null=True)
    address_complement = models.CharField(max_length=120, blank=True, null=True)
    state = models.CharField(max_length=50,blank=True, null=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(unique=True, null=False, blank=False)
    avatar = models.URLField(blank=True, null=True)
    biography = models.CharField(max_length=200,null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    updated_date = models.DateTimeField(auto_now=True)

    date_joined = models.DateTimeField(auto_now_add=True)

    validated_email = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % (super(DefaultUser, self).username)

class ForgotPassword(models.Model):
    user = models.OneToOneField(DefaultUser, on_delete=models.CASCADE, primary_key=True)
    token = models.CharField(max_length=200, null=True, blank=True, unique=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return "%s" % (self.token)

