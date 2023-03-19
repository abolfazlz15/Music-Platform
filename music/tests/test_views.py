from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from urllib.parse import urlencode

from accounts.models import User, Artist
from music.models import Category, Music, HomeSlider


class CateogryListViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('music:category_list')
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.category = Category.objects.create(title='test_category')

    def test_get_category_list_authorized(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category_list_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



class CateogryDetailViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        self.artist = Artist.objects.create(name='testArtist')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.category = Category.objects.create(title='test_category')
        self.music = Music.objects.create(title='test_title', url='https://test', text='test_text')
        self.music.category.set([self.category])
        self.music.artist.set([self.artist])

        self.url = reverse('music:category_detail', args=(self.category.id,))


    def test_get_category_detail_authorized(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category_detail_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        

class PopularMusicListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        self.artist = Artist.objects.create(name='testArtist')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.category = Category.objects.create(title='test_category')
        self.music = Music.objects.create(title='test_title', url='https://test', text='test_text')
        self.music.category.set([self.category])
        self.music.artist.set([self.artist])
        self.url = reverse('music:popular_music')

    def test_get_popular_music_list_authorized(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertAlmostEqual(response.status_code, status.HTTP_200_OK)

    def test_get_popular_music_list_unauthorized(self):
        response = self.client.get(self.url)
        self.assertAlmostEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)   


class RecentMusicListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        self.artist = Artist.objects.create(name='testArtist')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.category = Category.objects.create(title='test_category')
        self.music = Music.objects.create(title='test_title', url='https://test', text='test_text')
        self.music.category.set([self.category])
        self.music.artist.set([self.artist])
        self.url = reverse('music:recent_music')

    def test_get_recent_music_list_authorized(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertAlmostEqual(response.status_code, status.HTTP_200_OK)

    def test_get_recent_music_list_unauthorized(self):
        response = self.client.get(self.url)
        self.assertAlmostEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)   


class MusicByTrendCategoryListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        self.artist = Artist.objects.create(name='testArtist')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.category = Category.objects.create(title='trend')
        self.music = Music.objects.create(title='test_title', url='https://test', text='test_text')
        self.music.category.set([self.category])
        self.music.artist.set([self.artist])
        self.url = reverse('music:music_by_trend_category')

    def test_get_music_by_trend_category_list_authorized(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertAlmostEqual(response.status_code, status.HTTP_200_OK)

    def test_get_music_by_trend_category_list_unauthorized(self):
        response = self.client.get(self.url)
        self.assertAlmostEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)   


class SliderHomePageTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        self.artist = Artist.objects.create(name='testArtist')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.slider = HomeSlider.objects.create( url='https://test', status=True)
        self.url = reverse('music:slider_home_page')

    def test_get_slider_home_page_authorized(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertAlmostEqual(response.status_code, status.HTTP_200_OK)

    def test_get_slider_home_page_unauthorized(self):
        response = self.client.get(self.url)
        self.assertAlmostEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 



class MusicSearchViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.music1 = Music.objects.create(title='Song 1', cover='song1.jpg')
        self.music2 = Music.objects.create(title='Song 2', cover='song2.jpg')
        self.music3 = Music.objects.create(title='Another Song', cover='another_song.jpg')
        self.url = reverse('music:search_music')
    
    def test_music_search(self):
        params = {'search': 'song'}
        url_with_params = f"{self.url}?{urlencode(params)}"
        response = self.client.get(url_with_params, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data[0]['title'], 'Song 1')
        self.assertEqual(response.data[0]['cover'].split('/')[-1], 'song1.jpg')
        self.assertEqual(response.data[1]['title'], 'Song 2')
        self.assertEqual(response.data[1]['cover'].split('/')[-1], 'song2.jpg')
        self.assertEqual(response.data[2]['title'], 'Another Song')
        self.assertEqual(response.data[2]['cover'].split('/')[-1], 'another_song.jpg')
        
    def test_music_search_no_results(self):
        params = {'search': 'notfound'}
        url_with_params = f"{self.url}?{urlencode(params)}"
        response = self.client.get(url_with_params, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)


class MusicDetailViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        self.artist = Artist.objects.create(name='testArtist')
        self.category = Category.objects.create(title='test_category')
        self.music = Music.objects.create(title='test_title', url='https://test', text='test_text')
        self.music.category.set([self.category])
        self.music.artist.set([self.artist])
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.url = reverse('music:music_detail', args=(self.music.id,))

    def test_get_music_detail_authorized(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.music.title)

    def test_get_music_detail_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class InternationalMusicListTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        self.artist = Artist.objects.create(name='testArtist')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.category = Category.objects.create(title='test_category')
        self.music = Music.objects.create(title='test_title', url='https://test', text='test_text', type='International')
        self.music.category.set([self.category])
        self.music.artist.set([self.artist])
        self.url = reverse('music:international_music')

    def test_get_international_music_list_authorized(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertAlmostEqual(response.status_code, status.HTTP_200_OK)

    def test_get_international_music_list_unauthorized(self):
        response = self.client.get(self.url)
        self.assertAlmostEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)   
