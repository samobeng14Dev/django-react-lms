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
    path('user/change-password/',api_views.ChangePasswordAPIView.as_view(), name='change_password'),

    # Core Endpoints
    path('core/category/', api_views.CategoryListAPIView.as_view(),
         name='category_list_create'),
    path('core/course-list/', api_views.CourseListAPView.as_view(),
         name='course_list_create'),
    path('core/course-detail/<slug>/',
         api_views.CourseDetailAPIView.as_view(), name='course_detail'),
    path('course/cart/', api_views.CartAPIView.as_view(), name='cart'),  
    path('course/cart-list/<cart_id>/', api_views.CartListAPIView.as_view(), name='cart_list'), 
    path('course/cart-item-delete/<cart_id>/<item_id>/', api_views.CartItemDeleteAPIView.as_view(), name='cart_item_delete'),
    path('cart/cart-stats/<cart_id>/', api_views.CartStatsAPIView.as_view(), name='cart_stats'),
    path('order/create-order/', api_views.CreateOrderAPIView.as_view(), name='create_order'),
    path('order/checkout/<oid>/', api_views.CheckoutAPIView.as_view(), name='checkout'),
    path('order/coupon/', api_views.CouponApplyAPIView.as_view(), name='coupon'),
    path('payment/stripe-checkout/<oid>/', api_views.StripeCheckoutAPIView.as_view(), name='stripe_checkout'),
    path('payment/payment-success/', api_views.PaymentSuccessAPIView.as_view(), name='payment_success'),
    path('course/search/', api_views.SearchCourseAPIView.as_view(), name='course_search'),

#     Students API Endpoints
    path("student/summary/<user_id>/",
         api_views.StudentSummaryAPIView.as_view(), name="student_summary"),
    path('student/course-list/<user_id>/', api_views.StudentCourseListAPIView.as_view(), name='student_course_list'),
    path("student/course-detail/<user_id>/<enrollment_id>/",
         api_views.StudentCourseDetailAPIView.as_view(),name="student_course_detail"),
    path("student/course-completed/",
         api_views.StudentCourseCompletedCreateAPIView.as_view()),
    path("student/course-note/<user_id>/<enrollment_id>/",
         api_views.StudentNoteCreateAPIView.as_view()),
    path("student/course-note-detail/<user_id>/<enrollment_id>/<note_id>/",
         api_views.StudentNoteDetailAPIView.as_view()),
    path("student/rate-course/", api_views.StudentRateCourseCreateAPIView.as_view()),
    path("student/review-detail/<user_id>/<review_id>/",
          api_views.StudentRateCourseUpdateAPIView.as_view()),
#     path("student/wishlist/<user_id>/",
#          api_views.StudentWishListListCreateAPIView.as_view()),
#     path("student/question-answer-list-create/<course_id>/",
#          api_views.QuestionAnswerListCreateAPIView.as_view()),
#     path("student/question-answer-message-create/",
#          api_views.QuestionAnswerMessageSendAPIView.as_view()),



]
