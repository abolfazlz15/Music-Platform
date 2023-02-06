from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from accounts.api import views

app_name = 'accounts'
urlpatterns = [
    # JWT URL
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # login URL
    path('login', views.UserLoginView.as_view(), name='login'),
]