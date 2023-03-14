from django.utils.translation import gettext_lazy as _
from rest_framework.test import APITestCase

from music.models import Music, Category


class CategoryModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(title='test_category')

    def test_title_label(self):
        field_label = self.category._meta.get_field('title').verbose_name
        self.assertEqual(field_label, _('title'))

    def test_str_method(self):
        expected_result = self.category.title
        self.assertEqual(self.category.__str__(), expected_result) 
