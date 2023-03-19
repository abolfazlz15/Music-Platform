from django.utils.translation import gettext_lazy as _
from rest_framework.test import APITestCase

from music.models import Music, Category
from accounts.models import Artist


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

class NusicyModelTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.artist = Artist.objects.create(name='testArtist')
        cls.category = Category.objects.create(title='test_category')
        cls.music = Music.objects.create(title='test_title', url='https://test', text='test_text')
        cls.music.category.set([cls.category])
        cls.music.artist.set([cls.artist])
        
    def test_title_label(self):
        field_label = self.music._meta.get_field('title').verbose_name
        self.assertEqual(field_label, _('title'))

    def test_artist_label(self):
        field_label = self.music._meta.get_field('artist').verbose_name
        self.assertEqual(field_label, _('artist'))

    def test_url_label(self):
        field_label = self.music._meta.get_field('url').verbose_name
        self.assertEqual(field_label, _('url'))
    
    def test_text_label(self):
        field_label = self.music._meta.get_field('text').verbose_name
        self.assertEqual(field_label, _('text'))

    def test_category_label(self):
        field_label = self.music._meta.get_field('category').verbose_name
        self.assertEqual(field_label, _('category'))

    def test_type_label(self):
        field_label = self.music._meta.get_field('type').verbose_name
        self.assertEqual(field_label, _('type'))

    def test_str_method(self):
        expected_result = self.music.title
        self.assertEqual(self.music.__str__(), expected_result) 
