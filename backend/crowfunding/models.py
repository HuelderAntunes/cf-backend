from django.db import models
from backend.login.models import DefaultUser

class ProjectType(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Project(models.Model):
    author = models.ForeignKey(DefaultUser, on_delete=models.CASCADE)
    project_type = models.ForeignKey(ProjectType, on_delete=models.PROTECT)
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=250, null=True, blank=True)

    page_content = models.TextField(null=True, blank=True)

    target_found = models.FloatField(null=True, blank=True)
    sale_share_percent = models.FloatField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ProjectRolePermission(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name

class ProjectRole(models.Model):
    name = models.CharField(max_length=80)
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class ProjectPermission(models.Model):
    role_permission = models.ForeignKey(ProjectRolePermission, on_delete=models.CASCADE)
    project_role = models.ForeignKey(ProjectRole, on_delete=models.CASCADE)

    def __str__(self):
        return "%s to %s" % (self.role_permission.name, self.project_role.name)

class ProjectUser(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(DefaultUser, on_delete=models.CASCADE)
    role = models.ForeignKey(ProjectRole, on_delete=models.PROTECT)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s to %s" % (self.role.name, self.project.name)

class Donation(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(DefaultUser, on_delete=models.PROTECT)
    value = models.FloatField()

    message = models.TextField(null=True, blank=True)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s to %s" % (self.value, self.project.name)