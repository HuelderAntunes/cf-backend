from rest_framework.routers import DefaultRouter
from .views import DefaultUserViewSet, SessionViewSet

router = DefaultRouter()

router.register(r'users', DefaultUserViewSet, 'user')
router.register(r'sessions', SessionViewSet, 'session')