from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Artist, User
from music.models import Category, Music
from play_list.models import Playlist
from play_list.api.serializers import PlayListSerializer

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

    def test_get_playlist_detail_authorized(self):
        response = self.client.get(self.url,HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_playlist_detail_unauthorized(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


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



class UserUpdatePlayListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.music1 = Music.objects.create(title='test_title1', url='https://test1', text='test_text1')
        self.playlist = Playlist.objects.create(name='test', user=self.user)
        self.playlist.songs.set([self.music1])
        self.url = reverse('playlist:update_playlist', args=(self.playlist.id,))
        
    def test_update_playlist_authenticated(self):
        new_data = {
            'name': 'new name',
        }
        response = self.client.put(self.url, data=new_data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.playlist.refresh_from_db()
        self.assertEqual(self.playlist.name, new_data['name'])
        
    def test_update_playlist_unauthorized(self):
        # Create another user to simulate unauthorized access
        unauthorized_user = User.objects.create_user(
            email='unauthorized@example.com',
            username='unauthorized',
            password='testpassword',
        )
        refresh = RefreshToken.for_user(unauthorized_user)
        unauthorized_token = str(refresh.access_token)
        
        new_data = {
            'name': 'new name',
        }
        response = self.client.put(self.url, data=new_data, HTTP_AUTHORIZATION=f'Bearer {unauthorized_token}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserDeletePlayListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.music1 = Music.objects.create(title='test_title1', url='https://test1', text='test_text1')
        self.playlist = Playlist.objects.create(name='test', user=self.user)
        self.playlist.songs.set([self.music1])
        self.url = reverse('playlist:delete_playlist', args=(self.playlist.id,))
        
    def test_delete_playlist_authenticated(self):
        response = self.client.delete(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(Playlist.DoesNotExist):
            self.playlist.refresh_from_db()
            
    def test_delete_playlist_unauthorized(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PlaylistAddMusicViewTestCase(APITestCase):
    def setUp(self):
        self.artist = Artist.objects.create(name='testArtist')
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.playlist = Playlist.objects.create(
            user=self.user,
            name='Test Playlist'
        )
        self.music = Music.objects.create(title='test_title1', url='https://test1', text='test_text1')
        self.music.artist.set([self.artist])

        self.url = reverse('playlist:add_music_to_playlist', kwargs={'pk': self.playlist.pk})
        self.data = {'music_id': self.music.pk}

    def test_add_music_to_playlist(self):
        response = self.client.put(self.url, data=self.data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('result', response.data)
        self.assertIn('data', response.data)
        self.assertEqual(response.data['result'], 'music added')
        playlist = Playlist.objects.get(pk=self.playlist.pk)
        self.assertIn(self.music, playlist.songs.all())
        serializer = PlayListSerializer(playlist)
        self.assertEqual(response.data['data'], serializer.data)

    def test_add_invalid_music_to_playlist(self):
        response = self.client.put(self.url, data={'music_id': 999}, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Invalid music ID')

    def test_add_music_to_nonexistent_playlist(self):
        url = reverse('playlist:add_music_to_playlist', kwargs={'pk': 999})
        response = self.client.put(url, data=self.data,  HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Invalid playlist ID')


class PlaylistRemoveMusicViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        self.playlist = Playlist.objects.create(
            user=self.user,
            name='Test Playlist'
        )
        self.music = Music.objects.create(title='test_title1', url='https://test1', text='test_text1')
        self.playlist.songs.add(self.music)

        self.url = reverse('playlist:remove_music_from_playlist', kwargs={'pk': self.playlist.pk})
        self.data = {'music_id': self.music.pk}

    def test_remove_music_from_playlist(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIn('result', response.data)
        self.assertIn('data', response.data)
        self.assertEqual(response.data['result'], 'music remove')
        self.assertFalse(self.playlist.songs.filter(id=self.music.id).exists())
        serializer = PlayListSerializer(instance=self.playlist)
        self.assertEqual(response.data['data'], serializer.data)

    def test_remove_invalid_music_from_playlist(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.url, data={'music_id': 999})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Invalid music ID')

    def test_remove_music_from_nonexistent_playlist(self):
        url = reverse('playlist:remove_music_from_playlist', kwargs={'pk': 999})
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url, data=self.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'Invalid playlist ID')
