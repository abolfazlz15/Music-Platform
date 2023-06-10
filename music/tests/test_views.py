from urllib.parse import urlencode

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Artist, User
from music.api.serializers import MusicListSerializer
from music.models import Category, FavoriteMusic, HomeSlider, Music


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
        self.music.category = self.category
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
        self.music.category = self.category
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
        self.music.category = self.category
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
        self.music.category = self.category
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
        self.artist = Artist.objects.create(name='Artist 1', image='artist1.jpg')
        self.url = reverse('music:search_music')
    
    def test_music_search(self):
        params = {'search': 'song'}
        url_with_params = f"{self.url}?{urlencode(params)}"
        response = self.client.get(url_with_params, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the music results
        self.assertEqual(len(response.data['music']), 3)
        self.assertEqual(response.data['music'][0]['title'], 'Song 1')
        self.assertEqual(response.data['music'][0]['cover'].split('/')[-1], 'song1.jpg')
        self.assertEqual(response.data['music'][1]['title'], 'Song 2')
        self.assertEqual(response.data['music'][1]['cover'].split('/')[-1], 'song2.jpg')
        self.assertEqual(response.data['music'][2]['title'], 'Another Song')
        self.assertEqual(response.data['music'][2]['cover'].split('/')[-1], 'another_song.jpg')

        # Check the user results
        self.assertEqual(len(response.data['user']), 0)

        # Check the artist results
        self.assertEqual(len(response.data['artist']), 0)
        
    def test_music_search_with_artist(self):
        params = {'search': 'artist'}
        url_with_params = f"{self.url}?{urlencode(params)}"
        response = self.client.get(url_with_params, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check the music results
        self.assertEqual(len(response.data['music']), 0)

        # Check the user results
        self.assertEqual(len(response.data['user']), 0)

        # Check the artist results
        self.assertEqual(len(response.data['artist']), 1)
        self.assertEqual(response.data['artist'][0]['name'], 'Artist 1')
        self.assertEqual(response.data['artist'][0]['image'].split('/')[-1], 'artist1.jpg')
        
    def test_music_search_no_results(self):
        params = {'search': 'notfound'}
        url_with_params = f"{self.url}?{urlencode(params)}"
        response = self.client.get(url_with_params, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['music']), 0)
        self.assertEqual(len(response.data['user']), 0)
        self.assertEqual(len(response.data['artist']), 0)
    

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
        self.music.category = self.category
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
        self.music.category = self.category
        self.music.artist.set([self.artist])
        self.url = reverse('music:international_music')

    def test_get_international_music_list_authorized(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertAlmostEqual(response.status_code, status.HTTP_200_OK)

    def test_get_international_music_list_unauthorized(self):
        response = self.client.get(self.url)
        self.assertAlmostEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)   


class UserFavoriteMusicViewTestCase(APITestCase):
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


class UserFavoriteMusicViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.user = User.objects.create(username='testuser')
        self.music1 = Music.objects.create(title='test_title1', url='https://test1', text='test_text1')
        self.music2 = Music.objects.create(title='test_title2', url='https://test2', text='test_text2')
        self.favorite1 = FavoriteMusic.objects.create(user=self.user, music=self.music1)
        self.favorite2 = FavoriteMusic.objects.create(user=self.user, music=self.music2)
        self.url = reverse('music:user_favorite_music', kwargs={'pk': self.user.pk})
        

    def test_get_favorite_music_list_authorized(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        expected_data = MusicListSerializer([self.music1, self.music2], many=True).data
        self.assertEqual(response.data, expected_data)
        self.assertAlmostEqual(response.status_code, status.HTTP_200_OK)

    def test_get_favorite_music_list_unauthorized(self):
        response = self.client.get(self.url)
        self.assertAlmostEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
   

class UserAddFavoriteMusicViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.music = Music.objects.create(title='test_title', url='https://test', text='test_text')
        self.url = reverse('music:user_add_favorite_music')

    def test_add_favorite_music_authorized(self):
        response = self.client.post(self.url, data={'pk': self.music.pk}, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': True, 'result': 'like'})

        # Ensure the favorite music object has been created for the user
        self.assertTrue(FavoriteMusic.objects.filter(user=self.user, music=self.music).exists())

        # Test unliking the music
        response = self.client.post(self.url, data={'pk': self.music.pk}, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(FavoriteMusic.objects.filter(user=self.user, music=self.music).exists())

    def test_add_favorite_music_unauthorized(self):
        response = self.client.post(self.url, data={'pk': self.music.pk})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
