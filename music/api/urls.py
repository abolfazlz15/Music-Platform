from django.urls import path
from music.api import views

app_name = 'music'
urlpatterns = [
    path('morelike/', views.PopularMusicListView.as_view(), name='popular_music'),
]