from django.urls import resolve, reverse
from rest_framework.test import APITestCase

from accounts.models import Artist, User
from play_list.api import views
from music.models import Category, Music
from play_list.models import Playlist


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
        cls.playlist = Playlist.objects.create(name='test_playlist', user=cls.user)
        cls.playlist.songs.set([cls.music])

    def test_user_playlist_list(self):
        url = reverse('playlist:user_playlist', args=(self.user.id,))
        self.assertEqual(resolve(url).func.view_class, views.UserPlayListView)

    def test_playlist_detail(self):
        url = reverse('playlist:detail_playlist', args=(self.playlist.id,))
        self.assertEqual(resolve(url).func.view_class, views.UserDetailPlayListView)

    def test_create_playlist(self):
        url = reverse('playlist:add_playlist')
        self.assertEqual(resolve(url).func.view_class, views.UserCreatePlayListView)

    def test_update_playlist(self):
        url = reverse('playlist:update_playlist', args=(self.playlist.id,))
        self.assertEqual(resolve(url).func.view_class, views.UserUpdatePlayListView)