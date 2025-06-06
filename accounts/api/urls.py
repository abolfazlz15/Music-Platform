from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.api import views

app_name = "accounts"
urlpatterns = [
    # JWT URL
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # login URL
    path("login/", views.UserLoginView.as_view(), name="login"),
    # register URL
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path(
        "register/verify/",
        views.UserVerifyRegisterCodeView.as_view(),
        name="verify_register_otp",
    ),
    # user URL
    path("profile/<int:pk>", views.UserProfileView.as_view(), name="profile"),
    path(
        "profile/update", views.UserUpdateProfileView.as_view(), name="profile-update"
    ),
    path("profile/imagelist", views.ImageProfileListView.as_view(), name="image_list"),
    # change password URL
    path("password/update", views.ChangePasswordView.as_view(), name="password-update"),
    # artist
    path(
        "profile/artist/<int:pk>",
        views.ArtistProfileView.as_view(),
        name="profile-artist",
    ),
    # forgot password
    path("reset", views.ForgotPasswordView.as_view(), name="reset_password"),
    path(
        "reset/changepassword/<str:encoded_pk>/<str:token>",
        views.ResetPasswordView.as_view(),
        name="change_password",
    ),
    path(
        "reset/done", views.RestPasswordDoneView.as_view(), name="reset_password_done"
    ),
]
