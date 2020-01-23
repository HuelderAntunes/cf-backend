from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework import mixins
from .serializers import DefaultUserSerializer, SessionSerializer
from rest_framework import views
from rest_framework.response import Response
from .models import DefaultUser
from rest_framework_simplejwt.tokens import RefreshToken

class DefaultUserViewSet(ModelViewSet):
    queryset = DefaultUser.objects.all().order_by('-id')
    serializer_class = DefaultUserSerializer

    def get_permissions(self):
        if (self.action not in ['create']):
            self.permission_classes = [permissions.IsAuthenticated]
        return super(self.__class__, self).get_permissions()

    def list(self, request):
        return Response(DefaultUserSerializer(request.user).data)

    def retrieve(self, request, pk):
        if(int(request.user.id) == int(pk)):
            return Response(DefaultUserSerializer(request.user).data)
        else:
            return Response({"error": "Without permission."}, status.HTTP_401_UNAUTHORIZED)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()

class SessionViewSet(GenericViewSet):
    def create(self, request):
        serialized = SessionSerializer(data=request.data)
        if(serialized.is_valid()):
            username = serialized.data["username"]
            password = serialized.data["password"]
            users = DefaultUser.objects.filter(username=username)
            print(password)
            if(len(users)):
                if(users[0].check_password(password)):
                    refresh = RefreshToken.for_user(users[0])
                    return Response({
                                        "refresh": str(refresh),
                                        "access": str(refresh.access_token)
                                    }, status.HTTP_200_OK)

            return Response({"error": "The username or password is incorrect."}, status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Remember of include username and password in your request."}, status.HTTP_400_BAD_REQUEST)
