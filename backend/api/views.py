from django.shortcuts import render, redirect
from userauths.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.db import transaction

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
import stripe
import requests

stripe.api_key=settings.STRIPE_SECRET_KEY


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


class CartStatsAPIView(generics.RetrieveAPIView):
    serializer_class = api_serializers.CartSerializer
    permission_classes = [AllowAny]
    lookup_field = 'cart_id'

    def get(self, request, *args, **kwargs):
        cart_id = self.kwargs['cart_id']
        cart_items = api_models.Cart.objects.filter(cart_id=cart_id)

        # Using Python's sum() and comprehensions for cleaner aggregation
        total_price = sum(float(item.price) for item in cart_items)
        total_tax = sum(float(item.tax_fee) for item in cart_items)
        total_total = sum(round(float(item.total), 2) for item in cart_items)

        data = {
            'total_price': total_price,
            'total_tax': total_tax,
            'total_total': total_total
        }

        return Response(data, status=status.HTTP_200_OK)


class CreateOrderAPIView(generics.CreateAPIView):
    serializer_class = api_serializers.CartOrderSerializer
    permission_classes = [AllowAny]
    queryset = api_models.CartOrder.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data

        # Extract fields from request data
        full_name = data.get('full_name')
        email = data.get('email')
        country = data.get('country')
        cart_id = data.get('cart_id')
        user_id = data.get('user_id')

        # Fetch user if user_id is valid, otherwise set to None
        user = User.objects.filter(id=user_id).first(
        ) if user_id and user_id != "undefined" else None

        # Fetch cart items with related course and teacher data to optimize database queries
        cart_items = api_models.Cart.objects.filter(
            cart_id=cart_id).select_related('course__teacher')

        # Calculate totals using list comprehensions
        total_price = sum(Decimal(item.price) for item in cart_items)
        total_tax = sum(Decimal(item.tax_fee) for item in cart_items)
        total_initial_total = sum(Decimal(item.total) for item in cart_items)
        total_total = total_initial_total

        # Create order and order items inside an atomic transaction
        with transaction.atomic():
            order = api_models.CartOrder.objects.create(
                full_name=full_name,
                email=email,
                country=country,
                student=user,
                sub_total=total_price,
                tax_fee=total_tax,
                initial_total=total_initial_total,
                total=total_total,
            )

            # Add teachers and create order items
            teachers_set = set()
            for item in cart_items:
                api_models.CartOrderItem.objects.create(
                    order=order,
                    course=item.course,
                    price=item.price,
                    tax_fee=item.tax_fee,
                    total=item.total,
                    initial_total=item.total,
                    teacher=item.course.teacher
                )
                teachers_set.add(item.course.teacher)

            # Add all unique teachers to the order in one step
            order.teachers.add(*teachers_set)
            order.save()

        # Return success response
        return Response({'message': 'Order created successfully'}, status=status.HTTP_201_CREATED)

class CheckoutAPIView(generics.RetrieveAPIView):
    serializer_class=api_serializers.CartOrderSerializer
    queryset=api_models.CartOrder.objects.all()
    permission_classes=[AllowAny]
    lookup_field='oid' 


class CouponApplyAPIView(generics.CreateAPIView):
    serializer_class = api_serializers.CouponSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        # Extract data from request
        order_oid = request.data.get('order_oid')
        coupon_code = request.data.get('coupon_code')

        try:
            # Retrieve order and coupon
            order = api_models.CartOrder.objects.get(oid=order_oid)
            coupon = api_models.Coupon.objects.filter(code=coupon_code).first()

            # Handle coupon not found
            if not coupon:
                return Response({"message": "Coupon Not Found", "icon": "error"}, status=status.HTTP_404_NOT_FOUND)

            # Filter eligible order items (items linked to the coupon's teacher)
            order_items = api_models.CartOrderItem.objects.filter(
                order=order, teacher=coupon.teacher)

            # Apply coupon to eligible items
            discount_applied = False  # Track if we successfully apply the coupon

            '''order_items contains the cart items related to the order. This loop checks each item one by one.'''
            for item in order_items:
                '''This condition checks if the current coupon has not already been applied. If it hasn’t, we proceed to apply the discount.'''
                if coupon not in item.coupons.all():
                    discount = item.total * coupon.discount / 100

                    # Update item fields
                    item.total -= discount
                    item.price -= discount
                    item.saved += discount
                    item.applied_coupon = True
                    item.coupons.add(coupon)
                    item.save()

                    # Update order fields
                    order.coupons.add(coupon)
                    order.total -= discount
                    order.sub_total -= discount
                    order.saved += discount
                    order.save()

                    # Track coupon usage by user
                    coupon.used_by.add(order.student)

                    discount_applied = True
                    break  # Stop after applying the coupon once

            if discount_applied:
                return Response({"message": "Coupon Found and Activated", "icon": "success"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Coupon Already Applied", "icon": "warning"}, status=status.HTTP_200_OK)

        except api_models.CartOrder.DoesNotExist:
            return Response({"message": "Order Not Found", "icon": "error"}, status=status.HTTP_404_NOT_FOUND)


class StripeCheckoutAPIView(generics.CreateAPIView):
    serializer_class=api_serializers.CartOrderSerializer
    permission_classes=[AllowAny]

    def create(self,request,*args,**kwargs):

        order_id=self.kwargs['order_id']
        order=api_models.CartOrder.objects.get(oid=order_id)

        if not order:
            return Response({'message': 'order not found'},status=status.HTTP_404_NOT_FOUND)        
        
        try:
            checkout_session = stripe.checkout.Session.create(
                customer_email=order.email,
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': order.full_name,
                            },
                            'unit_amount': int(order.total * 100)
                        },
                        'quantity': 1
                    }
                ],
                mode='payment',
                success_url=settings.FRONTEND_SITE_URL + '/payment-success/' +
                order.oid + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.FRONTEND_SITE_URL + '/payment-failed/'
            )
            print("checkout_session ====", checkout_session)
            order.stripe_session_id = checkout_session.id

            return redirect(checkout_session.url)
        except stripe.error.StripeError as e:
            return Response({"message": f"Something went wrong when trying to make payment. Error: {str(e)}"})

# function based view
def get_access_token(client_id, secret_key):
    token_url = "https://api.sandbox.paypal.com/v1/oauth2/token"
    data = {'grant_type': 'client_credentials'}
    auth = (client_id, secret_key)
    response = requests.post(token_url, data=data, auth=auth)

    if response.status_code == 200:
        print("Access TOken ====", response.json()['access_token'])
        return response.json()['access_token']
    else:
        raise Exception(
            f"Failed to get access token from paypal {response.status_code}")


class PaymentSuccessAPIView(generics.CreateAPIView):
    serializer_class = api_serializers.CartOrderSerializer
    queryset = api_models.CartOrder.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        order_oid = request.data['order_oid']
        session_id = request.data['session_id']
        paypal_order_id = request.data['paypal_order_id']

        print("order_oid ====", order_oid)
        print("session_id ====", session_id)
        print("paypal_order_id ====", paypal_order_id)

        order = api_models.CartOrder.objects.get(oid=order_oid)
        order_items = api_models.CartOrderItem.objects.filter(order=order)

        # Paypal payment success
        if paypal_order_id != "null":
            paypal_api_url = f"https://api-m.sandbox.paypal.com/v2/checkout/orders/{paypal_order_id}"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f"Bearer {get_access_token(PAYPAL_CLIENT_ID, PAYPAL_SECRET_ID)}"
            }
            response = requests.get(paypal_api_url, headers=headers)
            if response.status_code == 200:
                paypal_order_data = response.json()
                paypal_payment_status = paypal_order_data['status']
                if paypal_payment_status == "COMPLETED":
                    if order.payment_status == "Processing":
                        order.payment_status = "Paid"
                        order.save()
                        api_models.Notification.objects.create(
                            user=order.student, order=order, type="Course Enrollment Completed")
                        for o in order_items:
                            api_models.Notification.objects.create(
                                teacher=o.teacher, order=order, order_item=o, type="New Order")
                            api_models.EnrolledCourse.objects.create(
                                course=o.course, user=order.student, teacher=o.teacher, order_item=o)

                        return Response({"message": "Payment Successfull"})
                    else:
                        return Response({"message": "Already Paid"})
                else:
                    return Response({"message": "Payment Failed"})
            else:
                return Response({"message": "PayPal Error Occured"})

        # Stripe payment success
        if session_id != 'null':
            session = stripe.checkout.Session.retrieve(session_id)
            if session.payment_status == "paid":
                if order.payment_status == "Processing":
                    order.payment_status = "Paid"
                    order.save()

                    api_models.Notification.objects.create(
                        user=order.student, order=order, type="Course Enrollment Completed")
                    for o in order_items:
                        api_models.Notification.objects.create(
                            teacher=o.teacher, order=order, order_item=o, type="New Order")
                        api_models.EnrolledCourse.objects.create(
                            course=o.course, user=order.student, teacher=o.teacher, order_item=o)

                    return Response({"message": "Payment Successfull"})
                else:
                    return Response({"message": "Already Paid"})
            else:
                return Response({"message": "Payment Failed"})
            
# class CouponApplyAPIView(generics.CreateAPIView):
#     serializer_class = api_serializers.CouponSerializer
#     permission_classes = [AllowAny]

#     def create(self, request, *args, **kwargs):
#         order_oid = request.data['order_oid']
#         coupon_code = request.data['coupon_code']

#         order = api_models.CartOrder.objects.get(oid=order_oid)
#         coupon = api_models.Coupon.objects.filter(code=coupon_code).first()

#         if coupon:
#             order_items = api_models.CartOrderItem.objects.filter(
#                 order=order, teacher=coupon.teacher)
#             for i in order_items:
#                 if not coupon in i.coupons.all():
#                     discount = i.total * coupon.discount / 100

#                     i.total -= discount
#                     i.price -= discount
#                     i.saved += discount
#                     i.applied_coupon = True
#                     i.coupons.add(coupon)

#                     order.coupons.add(coupon)
#                     order.total -= discount
#                     order.sub_total -= discount
#                     order.saved += discount

#                     i.save()
#                     order.save()
#                     coupon.used_by.add(order.student)
#                     return Response({"message": "Coupon Found and Activated", "icon": "success"}, status=status.HTTP_201_CREATED)
#                 else:
#                     return Response({"message": "Coupon Already Applied", "icon": "warning"}, status=status.HTTP_200_OK)
#         else:
#             return Response({"message": "Coupon Not Found", "icon": "error"}, status=status.HTTP_404_NOT_FOUND)
    




# class CreateOrderAPIView(generics.CreateAPIView):
#     serializer_class=api_serializers.CartSerializer
#     permission_classes=[AllowAny]
#     queryset=api_models.CartOrder.objects.all()

#     def create(self, request, *args, **kwargs):
#         full_name=request.data['full_name']
#         email=request.data['email']
#         country=request.data['country']
#         cart_id=request.data['cart_id']
#         user_id=request.data['user_id']

#         if user_id != 0 and user_id != "undefined":
#             user=User.objects.filter(id=user_id).first()    
#         else:
#             user=None    

#         cart_items=api_models.Cart.objects.filter(cart_id=cart_id)
#         total_price=Decimal(0.00)
#         total_tax=Decimal(0.00)
#         total_initial_total=Decimal(0.00)    
#         total_total=Decimal(0.00)

#         order=api_models.CartOrder.objects.create(
#             full_name=full_name,
#             email=email,
#             country=country,
#             student=user
#         )

#         for c in cart_items:
#             api_models.CartOrderItem.objects.create(
#                 order=order,
#                 course=c.course,
#                 price=c.price,
#                 tax_fee=c.tax_fee,
#                 total=c.total,
#                 initial_total=c.total,
#                 teacher=c.course.teacher
#             )
            
#             total_price+=Decimal(c.price)
#             total_tax+=Decimal(c.tax_fee)
#             total_initial_total+=Decimal(c.total)
#             total_total+=Decimal(c.total)

#             order.teachers.add(c.course.teacher)

#             order.sub_total=total_price
#             order.tax_fee=total_tax
#             order.initial_total=total_initial_total
#             order.total=total_total
#             order.save()    

#             return Response({'message':'Order created successfully'},status=status.HTTP_201_CREATED)
    

    

# class CartStatsAPIView(generics.RetrieveAPIView):
#     serializer_class=api_serializers.CartSerializer
#     permission_classes=[AllowAny]
#     lookup_field='cart_id'

#     def get_queryset(self):
#        cart_id = self.kwargs['cart_id']
#        queryset = api_models.Cart.objects.filter(cart_id=cart_id)
#        return queryset
    
#     def get(self,requests,*args,**kwargs):
#         query_set=self.get_queryset()

#         total_price=0.00
#         total_tax=0.00
#         total_total=0.00

#         for cart_item in query_set:
#            total_price+=float(self.calculate_price(cart_item))
#            total_tax+=float(self.calculate_tax(cart_item))
#            total_total+=round(float(self.calculate_total(cart_item)),2)

#         data={
#             'total_price':total_price,
#             'total_tax':total_tax,
#             'total_total':total_total
#         }   
#         return Response(data,status=status.HTTP_200_OK)

#     def calculate_price(self,cart_item):
#         return cart_item.price
#     def calculate_tax(self,cart_item):
#         return cart_item.tax_fee
#     def calculate_total(self,cart_item):
#         return cart_item.total

    
