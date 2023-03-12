from django.urls import resolve, reverse
from rest_framework.test import APITestCase

from accounts.api import views
from accounts.models import Artist, User


class TestUrls(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='test@gmail.com', username='test', password='test1234')
        
        cls.artist = Artist.objects.create(name='artistTest')


    def test_login(self):
        url = reverse('accounts:login')
        self.assertEqual(resolve(url).func.view_class, views.UserLoginView)

    def test_register(self):
        url = reverse('accounts:register')
        self.assertEqual(resolve(url).func.view_class, views.UserRegisterView)

    def test_register_check_otp(self):
        url = reverse('accounts:check-otp')
        self.assertEqual(resolve(url).func.view_class, views.GetOTPRegisterCodeView)
        
    def test_user_profile(self):
        url = reverse('accounts:profile', args=(self.user.id,))
        self.assertEqual(resolve(url).func.view_class, views.UserProfileView)

    def test_user_profile_update(self):
        url = reverse('accounts:profile-update')
        self.assertEqual(resolve(url).func.view_class, views.UserUpdateProfileView)

    def test_user_password_update(self):
        url = reverse('accounts:password-update')
        self.assertEqual(resolve(url).func.view_class, views.ChangePasswordView)

    def test_profile_artist(self):
        url = reverse('accounts:profile-artist', args=(self.artist.id,))
        self.assertEqual(resolve(url).func.view_class, views.ArtistProfileView)

    def test_artist_list(self):
        url = reverse('accounts:artist-all')
        self.assertEqual(resolve(url).func.view_class, views.ArtistListView)