from rest_framework.routers import DefaultRouter
from .views import DefaultUserViewSet, SessionViewSet, ForgotPasswordViewSet

router = DefaultRouter()

router.register(r'users', DefaultUserViewSet, 'user')
router.register(r'sessions', SessionViewSet, 'session')
router.register(r'forgotpassword', ForgotPasswordViewSet, 'forgotpassword')
