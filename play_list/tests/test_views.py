from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Artist, User
from music.models import Category, Music
from play_list.models import Playlist


class UserPlayListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.music1 = Music.objects.create(title='test_title1', url='https://test1', text='test_text1')
        self.playlist1 = Playlist.objects.create(name='test', user=self.user)
        self.playlist2 = Playlist.objects.create(name='test', user=self.user)
        self.playlist3 = Playlist.objects.create(name='test', user=self.user)
        self.playlist1.songs.set([self.music1])
        self.playlist2.songs.set([self.music1])
        self.playlist3.songs.set([self.music1])
        self.url = reverse('playlist:user_playlist', args=(self.user.id,))
        
    def test_get_user_playlist_authorized(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_playlist_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserDetailPlayListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        self.artist = Artist.objects.create(name='testArtist')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.music1 = Music.objects.create(title='test_title1', url='https://test1', text='test_text1')
        self.music2 = Music.objects.create(title='test_title2', url='https://test2', text='test_text2')
        self.music1.artist.set([self.artist])
        self.music2.artist.set([self.artist])
        self.playlist = Playlist.objects.create(name='test', user=self.user)
        self.playlist.songs.set([self.music1, self.music2])
        self.url = reverse('playlist:user_playlist', args=(self.playlist.user.id,))


    def test_get_category_detail_authorized(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_category_detail_authorized(self):
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)



class UserCreatePlayListViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = 'test@test.com'
        cls.username = 'test'
        cls.password = 'test1234'
        cls.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        cls.playlist = Playlist.objects.create(name='test', user=cls.user)
        refresh = RefreshToken.for_user(cls.user)
        cls.token = str(refresh.access_token)
        cls.url = reverse('playlist:add_playlist')


    def test_create_playlist_authorized(self):
        playlist = {
            'name': 'test_palylist',
            'user': self.user
        }
        response = self.client.post(self.url, data=playlist, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_create_playlist_unauthorized(self):
        playlist = {
            'name': 'test_palylist',
            'user': self.user,
        }
        response = self.client.post(self.url, data=playlist)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)