from django.db import models

class User(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    passwork_hash = models.CharField(max_length=255)
    avatar = models.URLField()