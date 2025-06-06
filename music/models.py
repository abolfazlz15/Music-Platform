from ckeditor.fields import RichTextField
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from music.managers import MusicManager
from accounts.models import Artist, User


class Category(models.Model):
    title = models.CharField(max_length=100, verbose_name=_("title"))
    image = models.ImageField(
        upload_to="image/category_image", null=True, blank=True, verbose_name=_("image")
    )

    class Meta:
        verbose_name = "دستبندی"
        verbose_name_plural = "دستبندی ها"

    def __str__(self):
        return self.title

    def show_cover(self):
        # show cover in admin panel
        if self.image:
            return format_html(
                f'<img src="{self.image.url}" alt="" width="50px" height="50px">'
            )
        else:
            return format_html("no cover")

    show_cover.short_description = "cover"


class Music(models.Model):
    MUSIC_TYPE = (
        ("International", "بین المللی"),
        ("Iranian", "ایرانی"),
    )
    title = models.CharField(max_length=150, verbose_name=_("title"))
    artist = models.ManyToManyField(
        Artist, related_name="musics", verbose_name=_("artist")
    )
    url = models.URLField(verbose_name=_("url"))
    music_file = models.FileField(
        upload_to="music/", null=True, blank=True, verbose_name=_("music file")
    )
    cover = models.ImageField(
        upload_to="image/music_cover",
        null=True,
        blank=True,
        verbose_name=_("music cover"),
    )
    text = RichTextField(verbose_name=_("text"), null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="musics",
        verbose_name=_("category"),
    )
    type = models.CharField(
        choices=MUSIC_TYPE,
        null=True,
        blank=True,
        default="Iranian",
        max_length=30,
        verbose_name=_("type"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    views = models.ManyToManyField(
        "IPAddress", related_name="musics", blank=True, verbose_name=_("views")
    )
    objects = MusicManager()

    class Meta:
        verbose_name = "موزیک"
        verbose_name_plural = "موزیک ها"

    def __str__(self):
        return self.title

    def show_cover(self):
        # show cover in admin panel
        if self.cover:
            return format_html(
                f'<img src="{self.cover.url}" alt="" width="50px" height="50px">'
            )
        else:
            return format_html("no cover")

    show_cover.short_description = "cover"

    def related_music(self):
        related_music_qs = (
            Music.objects.select_related("category")
            .prefetch_related("artist")
            .filter(category=self.category)
            .exclude(id=self.id)
            .order_by("?")[:10]
        )
        related_music = []
        ids = []
        for music in related_music_qs:
            if music.id not in ids:
                ids.append(music.id)
                related_music.append(music)
        return related_music


class FavoriteMusic(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favorite_musics",
        verbose_name=_("user"),
    )
    music = models.ForeignKey(
        Music,
        on_delete=models.CASCADE,
        related_name="favorite_musics",
        verbose_name=_("music"),
    )

    class Meta:
        verbose_name = "موزیک لایک شده کاربر"
        verbose_name_plural = "موزیک های لایک شده کاربر"

    def __str__(self):
        return f"{self.music.title} - {self.user.username}"


class ChooseMusicByCategory(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, null=True, blank=True
    )

    class Meta:
        verbose_name = "نمایش موزیک بر اساس دسته بندی در صفحه خانه"
        verbose_name_plural = "نمایش موزیک بر اساس دسته بندی در صفحه خانه"

    def __str__(self):
        return self.category.title


class HomeSlider(models.Model):
    image = models.ImageField(
        upload_to="image/home_slider_image", null=True, blank=True
    )
    url = models.URLField(null=True, blank=True)
    status = models.BooleanField(default=True)
    music_id = models.ForeignKey(Music, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "اسلایدر صفحه خانه"
        verbose_name_plural = "اسلایدر های صفحه خانه"


class IPAddress(models.Model):
    ip_address = models.GenericIPAddressField(verbose_name="ادرس آی پی")

    class Meta:
        verbose_name = "آدرس آی پی"
        verbose_name_plural = "آدرس های آی پی"

    def __str__(self):
        return self.ip_address
