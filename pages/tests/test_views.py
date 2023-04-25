from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from pages.api.serializers import TicketSerializer, TicketTitleListSerializer
from pages.models import Ticket, TicketTitle, AboutUs


class CreateTicketViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        self.ticket_title = TicketTitle.objects.create(title='test')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.url = reverse('page:create_ticket')


    def test_create_ticket(self):
        data = {'user': self.user.id, 'body': 'This is the body', 'title': self.ticket_title.id}
        response = self.client.post(self.url, data, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 1)
        ticket = Ticket.objects.get()
        self.assertEqual(ticket.user, self.user)
        self.assertEqual(ticket.body, data['body'])
        self.assertEqual(ticket.title, self.ticket_title)
        serializer = TicketSerializer(ticket)
        self.assertEqual(response.data, serializer.data)



class TicketTitleListViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        self.ticket_title = TicketTitle.objects.create(title='test')
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        self.url = reverse('page:ticket_title_list')
        TicketTitle.objects.create(title='test1')
        TicketTitle.objects.create(title='test2')
        TicketTitle.objects.create(title='دیگر')

    def test_get_ticket_title_list(self):
        
        response = self.client.get(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset = TicketTitle.objects.all().exclude(title='دیگر')
        third_object = TicketTitle.objects.get(title='دیگر')
        all_objects = list(queryset) + [third_object]
        serializer = TicketTitleListSerializer(instance=all_objects, many=True)
        self.assertEqual(response.data, serializer.data)




class AboutUsViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            username='test',
            password='testpassword',
        )
        self.about_us = AboutUs.objects.create(
            version='v1.0.0',
            description='test description'
        )
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

    def test_get_about_us(self):
        url = reverse('page:about_us')
        response = self.client.get(url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['version'], self.about_us.version)
        self.assertEqual(response.data['description'], self.about_us.description)
