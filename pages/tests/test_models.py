from django.utils.translation import gettext_lazy as _
from rest_framework.test import APITestCase

from pages.models import Ticket, TicketTitle, AboutUs
from accounts.models import User


class TicketTitleModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.title = TicketTitle.objects.create(title='test_title')

    def test_title_label(self):
        field_label = self.title._meta.get_field('title').verbose_name
        self.assertEqual(field_label, _('title'))


class TicketModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        cls.title = TicketTitle.objects.create(title='test_title')
        cls.ticket = Ticket.objects.create(user=cls.user, title=cls.title, body='test body')


    def test_user_label(self):
        field_label = self.ticket._meta.get_field('user').verbose_name
        self.assertEqual(field_label, _('user'))        

    def test_title_label(self):
        field_label = self.ticket._meta.get_field('title').verbose_name
        self.assertEqual(field_label, _('title'))                

    def test_body_label(self):
        field_label = self.ticket._meta.get_field('body').verbose_name
        self.assertEqual(field_label, _('body'))   


class AboutUsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.about_us = AboutUs.objects.create(
            version='v1.0.0',
            description='test description'
        )

    def test_version_label(self):
        field_label = self.about_us._meta.get_field('version').verbose_name
        self.assertEqual(field_label, _('version'))                

    def test_description_label(self):
        field_label = self.about_us._meta.get_field('description').verbose_name
        self.assertEqual(field_label, _('description'))   