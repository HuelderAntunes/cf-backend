from rest_framework.routers import DefaultRouter
from .views import UserViewSet, GroupViewSet

router = DefaultRouter()

router.register('group', GroupViewSet)
router.register('user', UserViewSet)