from django.shortcuts import render
from api import serializer as api_serializers
from rest_framework_simplejwt.views import TokenObtainPairView


class MytokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializers.MyTokenObtainPairSerializer