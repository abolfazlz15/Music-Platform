from django.urls import path
from rest_framework.routers import DefaultRouter

from play_list.api import views

app_name = 'playlist'
urlpatterns = [
    path('user/<int:pk>', views.UserPlayListView.as_view(), name='user_playlist'),
    path('detail/<int:pk>', views.UserDetailPlayListView.as_view(), name='detail_playlist'),
    path('add/', views.UserCreatePlayListView.as_view(), name='add_playlist'),
    path('update/<int:pk>', views.UserUpdatePlayListView.as_view(), name='update_playlist'),

]
