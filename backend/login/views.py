from django.contrib.auth.models import User, Group
from rest_framework.viewsets import ModelViewSet
from .serializers import GroupSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class UserViewSet(ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    permission_classes = (IsAuthenticatedOrReadOnly)

class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer