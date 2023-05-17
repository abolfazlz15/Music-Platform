from unittest.mock import MagicMock

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
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

    def test_update_user_unauthorized(self):
        url = reverse('accounts:profile-update')
        new_data = {
            'username': 'test2',
            }
        response = self.client.get(url, data=new_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ChangePasswordViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='test@test.com', username='test', password='TestPass1234')
        self.url = reverse('accounts:password-update')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

    def test_change_password_authorized(self):
        data = {'old_password': 'TestPass1234', 'new_password': 'NewTestPass1234!'}
        response = self.client.put(self.url, data, HTTP_AUTHORIZATION=f'Bearer {self.token}') 
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password_unauthorized(self):
        data = {'old_password': 'testpass123', 'new_password': 'newtestpass123'}
        response = self.client.put(self.url, data) 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_wrong_old_password(self):
        data = {'old_password': 'wrongpassword', 'new_password': 'newtestpass123'}
        response = self.client.put(self.url, data, HTTP_AUTHORIZATION=f'Bearer {self.token}') 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {'old_password': ['Wrong password.'], 'status': False})


class EmailTest(TestCase):
    def test_send_email(self):
        mail.send_mail('Subject here', 'Here is the message.',
            'from@example.com', ['to@example.com'],
            fail_silently=False)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Subject here')


class ForgotPasswordViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.forgot_password_url = reverse('accounts:reset_password')
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword'
        )

    def test_forgot_password_with_valid_email(self):
        data = {'email': 'testuser@example.com'}
        response = self.client.post(self.forgot_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_forgot_password_with_invalid_email(self):
        data = {'email': 'invalid@example.com'}
        response = self.client.post(self.forgot_password_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'], 'User does not exist')

        
class ResetPasswordViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.token = PasswordResetTokenGenerator().make_token(self.user)

    def test_reset_password_view(self):
        url = reverse('accounts:change_password', kwargs={'encoded_pk': self.uidb64, 'token': self.token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/forgot_password.html')
        
        new_password = 'new_test_password'
        form_data = {
            'new_password': new_password,
            'new_password_confirm': new_password,
        }
        response = self.client.post(url, form_data)
        self.assertEqual(response.status_code, 302) # redirected to reset_password_done view
        
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password(new_password))