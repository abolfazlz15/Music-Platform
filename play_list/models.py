from django.db import models
from music.models import Music

class PlayList(models.Model):
    music = models.ManyToManyField(Music, )