from rest_framework.test import APITestCase
from django.utils.translation import gettext_lazy as _
from accounts.models import User


class AuthorModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='test@test.com', username='test', password='test1234')

    def test_email_label(self):
        field_label = self.user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, _('email address'))

    def test_username_label(self):
        field_label = self.user._meta.get_field('username').verbose_name
        self.assertEqual(field_label, _('username'))

    def test_profile_image_label(self):
        field_label = self.user._meta.get_field('profile_image')

    def test_str_method(self):
        expected_result = self.user.email
        self.assertEqual(self.user.__str__(), expected_result)