from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from music.models import Music


class Playlist(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="playlists", verbose_name=_("user")
    )
    songs = models.ManyToManyField(
        Music, related_name="playlists", blank=True, verbose_name=_("songs")
    )

    class Meta:
        verbose_name = "پلی لیست"
        verbose_name_plural = "پلی لیست ها"

    def __str__(self):
        return self.name


class ApprovedPlaylist(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("name"))
    songs = models.ManyToManyField(
        Music, related_name="approved_playlists", blank=True, verbose_name=_("songs")
    )
    cover = models.ImageField(upload_to="image/palylist/cover")
    is_international = models.BooleanField(default=False)

    class Meta:
        verbose_name = "پلی لیست عمومی"
        verbose_name_plural = "پلی لیست های عمومی"

    def __str__(self):
        return self.name
