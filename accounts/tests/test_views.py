from unittest.mock import MagicMock

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Artist
from accounts.otp_service import OTP

User = get_user_model()

class UserLoginViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('accounts:login')
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        self.valid_payload = {
            'email': 'test@example.com',
            'full_name': 'test',
            'password': 'testpassword'
        }
        self.invalid_payload = {
            'email': 'test@example.com',
            'full_name': 'test',
            'password': 'invalidpassword'
        }

    def test_login_with_valid_credentials(self):
        response = self.client.post(
            self.url,
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(
            self.url,
            data=self.invalid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

class UserRegisterViewTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('accounts:register')
        self.valid_payload = {
            'email': 'testuser@example.com',
            'username': 'testuser',
            'password': 'testpassword123'
        }
        self.invalid_payload = {
            'email': 'invalidemail',
            'username': '',
            'password': ''
        }

    def test_register_user_with_valid_payload(self):
        mock_otp_generate = OTP.generate_otp = MagicMock(return_value='123456')
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(mock_otp_generate.call_count, 1)

    def test_register_user_with_invalid_payload(self):
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_register_user_with_missing_fields(self):
        response = self.client.post(self.url, {'email': 'test@example.com'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)



class UserProfileViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = 'test@test.com'
        cls.username = 'test'
        cls.password = 'test1234'
        cls.user = User.objects.create_user(email='test@test.com', username='test', password='test1234')
        refresh = RefreshToken.for_user(cls.user)
        cls.token = str(refresh.access_token)

    def test_get_profile_user(self):
        url = reverse('accounts:profile', args=(self.user.id,))
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ArtistProfileViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = 'test@test.com'
        cls.username = 'test'
        cls.password = 'test1234'
        cls.user = User.objects.create_user(email='test@test.com', username='test', password='test1234')
        cls.artist = Artist.objects.create(name='testArtist')
        refresh = RefreshToken.for_user(cls.user)
        cls.token = str(refresh.access_token)

    def test_get_profile_user(self):
        url = reverse('accounts:profile-artist', args=(self.artist.id,))
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserUpdateProfileViewTestCase(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.email = 'test@test.com'
        cls.username = 'test'
        cls.password = 'test1234'
        cls.user = User.objects.create_user(email='test@test.com', username='test', password='test1234')
        cls.artist = Artist.objects.create(name='testArtist')
        refresh = RefreshToken.for_user(cls.user)
        cls.token = str(refresh.access_token)

    def test_update_user_authorized(self):
        url = reverse('accounts:profile-update')
        new_data = {
            'username': 'test2',
        }
        response = self.client.put(url, data=new_data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], new_data['username'])

    def test_update_user_unauthorized(self):
        url = reverse('accounts:profile-update')
        new_data = {
            'username': 'test2',
            }
        response = self.client.get(url, data=new_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)