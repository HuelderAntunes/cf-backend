from rest_framework.routers import DefaultRouter
from .views import UserViewSet, GroupViewSet

router = DefaultRouter()

router.register('groups', GroupViewSet, 'group')
router.register('users', UserViewSet, 'user')