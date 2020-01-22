from django.contrib import admin
from .models import Donation, Project, ProjectRole, ProjectRolePermission, ProjectType, ProjectUser, ProjectPermission

admin.site.register(Project)
admin.site.register(Donation)
admin.site.register(ProjectRole)
admin.site.register(ProjectRolePermission)
admin.site.register(ProjectType)
admin.site.register(ProjectUser)
admin.site.register(ProjectPermission)