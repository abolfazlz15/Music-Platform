from django.utils.translation import gettext_lazy as _
from rest_framework.test import APITestCase
from accounts.models import User
from play_list.models import Playlist
from music.models import Music


class PlayListModelTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='test_password',
        )
        self.song1 = Music.objects.create(title='test_title', url='https://test', text='test_text')
        self.song2 = Music.objects.create(title='test_title2', url='https://test2', text='test_text2')
        self.playlist = Playlist.objects.create(name='test_playlist', user=self.user)
        self.playlist.songs.set([self.song1, self.song2])

    def test_name_label(self):
        field_label = self.playlist._meta.get_field('name').verbose_name
        self.assertEqual(field_label, _('name'))

    def test_user_label(self):
        field_label = self.playlist._meta.get_field('user').verbose_name
        self.assertEqual(field_label, _('user'))    


    def test_songs_label(self):
        field_label = self.playlist._meta.get_field('songs').verbose_name
        self.assertEqual(field_label, _('songs'))    


    def test_str_method(self):
        expected_result = self.playlist.name
        self.assertEqual(self.playlist.__str__(), expected_result)
