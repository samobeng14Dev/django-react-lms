from django.shortcuts import render
from api import serializer as api_serializers
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from userauths.models import User
from rest_framework.permissions import AllowAny


class MytokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializers.MyTokenObtainPairSerializer


class RegisterView(generics.GenericAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = api_serializers.RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
