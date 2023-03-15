from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User, Artist
from music.models import Category, Music


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

