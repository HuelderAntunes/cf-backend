from django.contrib import admin
from .models import DefaultUser, ForgotPassword

admin.site.register(DefaultUser)
admin.site.register(ForgotPassword)
