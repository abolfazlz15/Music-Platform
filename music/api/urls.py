from django.urls import path

from music.api import views



app_name = 'music'
urlpatterns = [
    path('morelike/', views.PopularMusicListView.as_view(), name='popular_music'),
    path('recentmusic/', views.RecentMusicListView.as_view(), name='recent_music'),
    path('musicbycategory/', views.MusicByCategoryListView.as_view(), name='music_by_category'),
]