from django.urls import path

from music.api import views

app_name = 'music'
urlpatterns = [
    path('morelike/', views.PopularMusicListView.as_view(), name='popular_music'),
    path('recentmusic/', views.RecentMusicListView.as_view(), name='recent_music'),
    path('musicbycategory/', views.MusicByCategoryListView.as_view(), name='music_by_category'),
    path('trendmusic/', views.MusicByTrendCategoryListView.as_view(), name='music_by_trend_category'),
    path('sliderhomepage/', views.SliderHomePage.as_view(), name='slider_home_page'),

    path('internationals/', views.InternationalMusicList.as_view(), name='international_music'),
    path('favoritemusic/', views.UserFavoriteMusicView.as_view(), name='user_favorite_music'),

    path('detail/<int:pk>/', views.MusicDetailView.as_view(), name='music_detail'),

    path('search/', views.MusicSearchView.as_view(), name='test'),

    # category URL
    path('category/', views.CateogryListView.as_view(), name='category_list'),
    path('category/detail/<int:pk>', views.CategoryDetailView.as_view(), name='category_detail'),

]