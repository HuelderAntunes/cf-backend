from uuid import uuid4
import bcrypt
from rest_framework.decorators import action
from django.contrib.auth.hashers import make_password
from rest_framework.viewsets import ModelViewSet, GenericViewSet, ViewSet
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework import mixins
from .serializers import *
from rest_framework import views
from rest_framework.response import Response 
from .models import DefaultUser, ForgotPassword
from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

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
            return Response({'error': 'Without permission.'}, status.HTTP_401_UNAUTHORIZED)

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()

class SessionViewSet(ViewSet):
    def create(self, request):
        serialized = SessionSerializer(data=request.data)
        if(serialized.is_valid()):
            username = serialized.data['username']
            password = serialized.data['password']
            users = DefaultUser.objects.filter(username=username)
            print(password)
            if(len(users)):
                if(users[0].check_password(password)):
                    refresh = RefreshToken.for_user(users[0])
                    return Response({
                                        'refresh': str(refresh),
                                        'access': str(refresh.access_token)
                                    }, status.HTTP_200_OK)

            return Response({'error': 'The username or password is incorrect.'}, status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Invalid fields.'}, status.HTTP_400_BAD_REQUEST)

class ForgotPasswordViewSet(ViewSet):
    def create(self, request):
        forgot_pass = ForgotPasswordSerializer(data=request.data)
        if(forgot_pass.is_valid()):
            try:
                user = DefaultUser.objects.get(email=forgot_pass.data["email"])
                text_token = str(uuid4())
                token = bytes(text_token, 'utf-8')
                hashed_token = str(bcrypt.hashpw(token, bcrypt.gensalt()), 'utf-8')
                forgot, created = ForgotPassword.objects.get_or_create(user=user)
                forgot.token = hashed_token
                forgot.save()

                # mail
                subject = 'Password Reset'
                sender = '02630358ef-56e3a1@inbox.mailtrap.io'
                mail = EmailMultiAlternatives()
                recipient = forgot_pass.data['email']

                context = { 'first_name':  user.first_name,
                           'token': text_token }

                text_content = render_to_string('forgotpassword.txt', context,request=request)
                html_content = render_to_string('forgotpassword.html', context, request=request)

                email = EmailMultiAlternatives(subject=subject,
                                               body=text_content,
                                               from_email=sender,
                                               to=[recipient],
                                               reply_to=[sender])
                email.attach_alternative(html_content, "text/html")
                email.send(fail_silently=False)

            except DefaultUser.DoesNotExist:
                pass

            return Response({'success': 'If user with provided email exists a link with password reset as been sent.'})

        return Response({'error': 'Invalid fields.'})

    @action(detail=False, methods=['post'])
    def recover(self, request):
        recover_pass = RecoverPasswordSerializer(data=request.data)
        if(recover_pass.is_valid()):
            try:
                user = DefaultUser.objects.get(email=recover_pass.data['email'])
                forgot_password = ForgotPassword.objects.get(user=user)
                hashed = bytes(forgot_password.token, 'utf-8')
                token = bytes(recover_pass.data["token"], 'utf-8')

                if(bcrypt.checkpw(token, hashed)):
                    user.set_password(recover_pass.data['new_password'])
                    forgot_password.delete()
                    return Response({'success': 'Password successfully setted!'})
                else:
                    return Response({'error': 'Invalid token!'})
            except DefaultUser.DoesNotExist:
                pass
            except ForgotPassword.DoesNotExist:
                pass
        return Response({'error': 'Invalid fields.'})
