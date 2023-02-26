from django.urls import path

from play_list.api import views

from rest_framework.routers import DefaultRouter


app_name = 'playlist'
urlpatterns = [
    path('user/<int:pk>', views.UserPlayListView.as_view(), name='user_playlist'),
    path('detail/<int:pk>', views.UserDetailPlayListView.as_view(), name='detail_music'),
    path('add/', views.UserCreatePlayListView.as_view(), name='add_music'),

]
