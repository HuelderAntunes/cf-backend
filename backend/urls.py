from django.contrib import admin
from django.urls import path, include
from backend.login.urls import router as login_router

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(login_router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
