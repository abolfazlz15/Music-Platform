from unittest.mock import MagicMock

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.otp_service import OTP


User = get_user_model()

class UserLoginViewTestCase(APITestCase):
    def setUp(self):
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
        url = reverse('accounts:login')
        response = self.client.post(
            url,
            data=self.valid_payload,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)

    def test_login_with_invalid_credentials(self):
        url = reverse('accounts:login')
        response = self.client.post(
            url,
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

    def test_register_user_with_existing_email(self):
        # Create a user with the same email as in the valid payload
        User.objects.create_user(email=self.valid_payload['email'], username='existinguser', password='existingpassword')
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data['email'][0], 'user with this email already exists.')