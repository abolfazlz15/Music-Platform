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

    # register URL
    path('register', views.UserRegisterView.as_view(), name='register'),
    path('check', views.GetOTPRegisterCodeView.as_view(), name='check-otp'),

    # user URL
    path('profile/<int:pk>', views.UserProfileView.as_view(), name='profile'),
    path('profile/update', views.UserUpdateProfileView.as_view(), name='profile-update'),


]