from django.db import models
from backend.login.models import DefaultUser

class Project(models.Model):
    author = models.ForeignKey(DefaultUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=250)

    page_content = models.TextField()

    target_found = models.DecimalField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

class ProjectRolePermission(models.Model):
    name = models.CharField(max_length=80)

class ProjectRole(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200)

class ProjectUser(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(DefaultUser, on_delete=models.CASCADE)
    role = models.ForeignKey(ProjectRole, on_delete=models.PROTECT)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

class Donation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(DefaultUser, on_delete=models.PROTECT)
    value = models.DecimalField()

    message = models.TextField()

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)