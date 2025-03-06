import random
from django.shortcuts import render
from api import serializer as api_serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from userauths.models import User
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class MytokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializers.MyTokenObtainPairSerializer


class RegisterView(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = api_serializers.RegisterSerializer


def generate_random_otp(length=7):
    otp = "".join([str(random.randint(0, 9)) for _ in range(length)])
    return otp


class PasswordResetEmailVerifyAPIView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializers.UserSerializer

    def get_object(self):
        email = self.kwargs['email']  # get the email from the url

        # get the user with the email
        user = User.objects.filter(email=email).first()

        if user:
            refresh = RefreshToken.for_user(user)
            uuid64 = user.pk
            refresh_token = str(refresh.access_token)

            user.refresh_token = refresh_token
            user.otp = generate_random_otp()
            user.save()
            link = f"http://localhost:5173/create-new-password/?otp={user.otp}&uuid64={uuid64}&refresh_token={refresh_token}"
           
        return user

class PasswordChangeAPIView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializers.UserSerializer

    def create(self, request,*args,**kwargs):
        payload = request.data

        otp= payload['otp']
        uuid64 = payload['uuid64']
        password= payload['password']

        user= User.objects.get(id=uuid64,otp=otp)
        if user:
            user.set_password(password)
            user.otp=''
            user.save()

            return Response({'message':'Password changed successfully'},status=status.HTTP_201_CREATED)
        else:
            return Response({'message':'User does not exist'},status=status.HTTP_404_NOT_FOUND)
           
  