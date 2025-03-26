from api import views as api_views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshSlidingView

urlpatterns = [
    # Authentication endpoints
    path('user/token/', api_views.MytokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('user/token/refresh/',
         TokenRefreshSlidingView.as_view(), name='token_refresh'),
    path('user/register/', api_views.RegisterView.as_view(), name='register'),
    path('user/password-reset/<str:email>/',
         api_views.PasswordResetEmailVerifyAPIView.as_view(), name='password_reset_email_verify'),
    path('user/password-change/',
         api_views.PasswordChangeAPIView.as_view(), name='password_change'),

    # Core Endpoints
    path('core/category/', api_views.CategoryListAPIView.as_view(),
         name='category_list_create'),
    path('core/course-list/', api_views.CourseListAPView.as_view(),
         name='course_list_create'),
    path('core/course/<slug>/',
         api_views.CourseDetailAPIView.as_view(), name='course_detail'),
    path('course/cart/', api_views.CartAPIView.as_view(), name='cart'),  
    path('course/cart-list/<cart_id>', api_views.CartListAPIView.as_view(), name='cart_list'), 
    path('course/cart-item-delete/<cart_id>/<item_id>', api_views.CartItemDeleteAPIView.as_view(), name='cart_item_delete'),
    path('cart/cart-stats/<cart_id>', api_views.CartStatsAPIView.as_view(), name='cart_stats'),
    path('order/create-order/', api_views.CreateOrderAPIView.as_view(), name='create_order'),
    path('order/checkout/<oid>', api_views.CheckoutAPIView.as_view(), name='checkout'),
    path('order/coupon/', api_views.CouponApplyAPIView.as_view(), name='coupon'),
]
