from django.db import models
from accounts.models import Artist
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField


class Category(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='image/category_image')

    def __str__(self):
        return self.title


class Music(models.model):
    title = models.CharField(max_length=150)
    artist = models.ManyToManyField(Artist, related_name='musics', verbose_name=_('artist'))
    url = models.URLField(verbose_name=_('url'))
    cover = models.ImageField(upload_to='image/music_cover', null=True, blank=True, verbose_name=_('music cover'))
    text = RichTextField(verbose_name=_('text'), null=True, blank=True)
    category = models.ManyToManyField(Category, related_name='musics', verbose_name=_('category'))

    def __str__(self):
        return f'{self.title} - {self.artist.name}'
