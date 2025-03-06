from api import views as api_views
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshSlidingView

urlpatterns = [
    path('user/token/', api_views.MytokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('user/token/refresh/', TokenRefreshSlidingView.as_view(), name='token_refresh'),
    path('user/register/', api_views.RegisterView.as_view(), name='register'),
]
