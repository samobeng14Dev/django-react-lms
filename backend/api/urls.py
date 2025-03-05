from api import views as api_views
from django.urls import path

urlpatterns = [
    path('user/token/', api_views.MytokenObtainPairView.as_view(), name='token_obtain_pair'),
]
