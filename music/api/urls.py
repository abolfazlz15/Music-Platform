from django.urls import path

from music.api import views



app_name = 'music'
urlpatterns = [
    path('morelike/', views.PopularMusicListView.as_view(), name='popular_music'),
    path('recentmusic/', views.RecentMusicListView.as_view(), name='recent_music'),
    path('musicbycategory/', views.MusicByCategoryListView.as_view(), name='music_by_category'),
    path('trendmusic/', views.MusicByTrendCategoryListView.as_view(), name='music_by_trend_category'),
    path('sliderhomepage/', views.SliderHomePage.as_view(), name='slider_home_page'),

    path('detail/<int:pk>/', views.MusicDetailView.as_view(), name='music_detail'),

    # category URL
    path('category/', views.CateogryListView.as_view(), name='category_list'),

]