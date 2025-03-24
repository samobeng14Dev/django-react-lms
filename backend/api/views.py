from django.shortcuts import render
from userauths.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from api import models as api_models
from api import serializer as api_serializers


from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics

import random
from decimal import Decimal


class MytokenObtainPairView(TokenObtainPairView):
    serializer_class = api_serializers.MyTokenObtainPairSerializer


class RegisterView(generics.CreateAPIView):
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

            context = {
                "link": link,
                "username": user.username
            }
            subject = "Password Reset"
            text_body = render_to_string('email/password_reset.txt', context)
            html_body = render_to_string('email/password_reset.html', context)

            msg = EmailMultiAlternatives(
                subject=subject,
                from_email=settings.FROM_EMAIL,
                to=[user.email]
            )
            msg.attach_alternative(html_body, "text/html")
            msg.send()
        return user


class PasswordChangeAPIView(generics.UpdateAPIView):
    permission_classes = [AllowAny]
    serializer_class = api_serializers.UserSerializer

    def create(self, request: Request, *args, **kwargs):
        payload = request.data

        otp = payload['otp']
        uuid64 = payload['uuid64']
        password = payload['password']

        user = User.objects.get(id=uuid64, otp=otp)
        if user:
            user.set_password(password)
            user.otp = ''
            user.save()

            return Response({'message': 'Password changed successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)


class CategoryListAPIView(generics.ListAPIView):
    queryset = api_models.Category.objects.filter(active=True)
    serializer_class = api_serializers.CategorySerializer
    permission_classes = [AllowAny]


class CourseListAPView(generics.ListAPIView):
    queryset = api_models.Course.objects.filter(
        platform_status='published', teacher_course_status='published')
    serializer_class = api_serializers.CourseSerializer
    permission_classes = [AllowAny]

class CourseDetailAPIView(generics.RetrieveAPIView):
    queryset = api_models.Course.objects.filter(
        platform_status='published', teacher_course_status='published')
    serializer_class = api_serializers.CourseSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        slug = self.kwargs['slug']
        course = api_models.Course.objects.get(slug=slug, platform_status='published', teacher_course_status='published')
        return course


class CartAPIView(generics.CreateAPIView):
    serializer_class = api_serializers.CartSerializer
    queryset=api_models.Cart.objects.all()
    permission_classes = [AllowAny]

    def create(self, request: Request, *args, **kwargs):
       
       """This retrieves the necessary fields (course_id, user_id, price, country, and cart_id) from the incoming request payload."""
       course_id=request.data["course_id"]
       user_id=request.data["user_id"]
       price=request.data["price"]
       country_name=request.data["country"]
       cart_id=request.data["cart_id"]

       """This filters the Course model to get the first object matching the provided course_id. It returns None if no match is found."""

       course=api_models.Course.objects.filter(id=course_id).first()

       """This checks if the user_id is not undefined. If it’s not, it filters the User model to get the first object matching the provided user_id. It returns None if no match is found. If the user_id is undefined, it sets the user to None."""

       if user_id != "undefined":
           user = User.objects.filter(id=user_id).first()
       else:
           user=None

       """This checks if the country exists in the Country model. If it does, it sets the country variable to the country name. If it doesn’t, it returns a 404 status code with a message."""

       try:
           country_object = api_models.Country.objects.filter(name=country_name).first()
           country=country_object.name

       except api_models.Country.DoesNotExist:
           return Response({'message': 'Country does not exist'}, status=status.HTTP_404_NOT_FOUND)

       if country_object:
           tax_rate=country_object.tax_rate/100
       else: 
           tax_rate=0



           '''This checks if there’s an existing cart with the given cart_id and course.If a cart is found, it updates the cart. If no cart is found, it creates a new one.'''

       cart=api_models.Cart.objects.filter(cart_id=cart_id, course=course).first()  

       if cart:
           cart.course=course
           cart.user=user
           cart.price=price
           cart.tax_fee=Decimal(price)*Decimal(tax_rate)
           cart.country=country      
           cart.cart_id=cart_id
           cart.total=Decimal(cart.price)+Decimal(cart.tax_fee)  
           cart.save()

           return Response({'message': 'Cart updated successfully'}, status=status.HTTP_200_OK)
       else:
           cart=api_models.Cart.objects.create(course=course, user=user, price=price, tax_fee=Decimal(price)*Decimal(tax_rate), country=country, cart_id=cart_id, total=Decimal(price)+Decimal(price)*Decimal(tax_rate))

           return Response({'message': 'Cart created successfully'}, status=status.HTTP_201_CREATED)

class CartListAPIView(generics.ListAPIView):
    serializer_class = api_serializers.CartSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
       cart_id=self.kwargs['cart_id']  
       queryset = api_models.Cart.objects.filter(cart_id=cart_id)
       return queryset

class CartItemDeleteAPIView(generics.DestroyAPIView):
    
    serializer_class = api_serializers.CartSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        cart_id=self.kwargs['cart_id']  
        item_id=self.kwargs['item_id']

        return api_models.Cart.objects.filter(cart_id=cart_id, id=item_id).first()
        
    
