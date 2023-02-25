from django.urls import path

from play_list.api import views



app_name = 'music'
urlpatterns = [
    path('user/<int:pk>', views.UserPlayListView.as_view(), name='user_playlist'),


]