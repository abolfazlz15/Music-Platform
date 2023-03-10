from django.urls import resolve, reverse
from rest_framework.test import APITestCase
from music.models import Category
from music.api import views

class TestUrls(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(title='test_category')

    def test_category_list(self):
        url = reverse('music:category_list')
        self.assertEqual(resolve(url).func.view_class, views.CateogryListView)

    def test_category_detail(self):
        url = reverse('music:category_detail', args=(self.category.id,))
        self.assertEqual(resolve(url).func.view_class, views.CategoryDetailView)

