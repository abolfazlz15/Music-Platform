from django.urls import resolve, reverse
from rest_framework.test import APITestCase

from accounts.models import Artist, User
from music.api import views
from music.models import Category, Music, FavoriteMusic


class TestUrls(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        cls.artist = Artist.objects.create(name='testArtist')
        cls.category = Category.objects.create(title='test_category')
        cls.music = Music.objects.create(title='test_title', url='https://test', text='test_text')
        cls.music.category.set([cls.category])
        cls.music.artist.set([cls.artist])
        cls.favorite_music = FavoriteMusic.objects.create(music=cls.music, user=cls.user)

    def test_category_list(self):
        url = reverse('music:category_list')
        self.assertEqual(resolve(url).func.view_class, views.CateogryListView)

    def test_category_detail(self):
        url = reverse('music:category_detail', args=(self.category.id,))
        self.assertEqual(resolve(url).func.view_class, views.CategoryDetailView)

    def test_popular_music(self):
        url = reverse('music:popular_music')
        self.assertEqual(resolve(url).func.view_class, views.PopularMusicListView)
    
    def test_recent_music(self):
        url = reverse('music:recent_music')
        self.assertEqual(resolve(url).func.view_class, views.RecentMusicListView)

    def test_music_by_trend_category(self):
        url = reverse('music:music_by_trend_category')
        self.assertEqual(resolve(url).func.view_class, views.MusicByTrendCategoryListView)

    def test_slider_home_page(self):
        url = reverse('music:slider_home_page')
        self.assertEqual(resolve(url).func.view_class, views.SliderHomePage)    
            
    def test_search_music(self):
        url = reverse('music:search_music')
        self.assertEqual(resolve(url).func.view_class, views.MusicSearchView) 
         
    def test_international_music(self):
        url = reverse('music:international_music')
        self.assertEqual(resolve(url).func.view_class, views.InternationalMusicList)    
         
    def test_user_favorite_music(self):
        url = reverse('music:user_favorite_music', args=(self.favorite_music.id,))
        self.assertEqual(resolve(url).func.view_class, views.UserFavoriteMusicView)   

    def test_user_add_favorite_music(self):
        url = reverse('music:user_add_favorite_music')
        self.assertEqual(resolve(url).func.view_class, views.UserAddFavoriteMusicView)       