from django.urls import resolve, reverse
from rest_framework.test import APITestCase
from pages.api import views

class TestUrls(APITestCase):
    def test_ticket_title_list(self):
        url = reverse('page:ticket_title_list')
        self.assertEqual(resolve(url).func.view_class, views.TicketTitleListView)

    def test_ticket_create(self):
        url = reverse('page:create_ticket')
        self.assertEqual(resolve(url).func.view_class, views.CreateTicketView)
