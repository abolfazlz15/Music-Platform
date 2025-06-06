# Generated by Django 4.1.6 on 2023-02-14 10:04

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("accounts", "0004_alter_user_profile_image"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("image", models.ImageField(upload_to="image/category_image")),
            ],
        ),
        migrations.CreateModel(
            name="Music",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=150)),
                ("url", models.URLField(verbose_name="url")),
                (
                    "cover",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="image/music_cover",
                        verbose_name="music cover",
                    ),
                ),
                (
                    "text",
                    ckeditor.fields.RichTextField(
                        blank=True, null=True, verbose_name="text"
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        blank=True,
                        choices=[
                            ("International", "بین المللی"),
                            ("Iranian", "ایرانی"),
                        ],
                        default="Iranian",
                        max_length=30,
                        null=True,
                        verbose_name="type",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "artist",
                    models.ManyToManyField(
                        related_name="musics",
                        to="accounts.artist",
                        verbose_name="artist",
                    ),
                ),
                (
                    "category",
                    models.ManyToManyField(
                        related_name="musics",
                        to="music.category",
                        verbose_name="category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FavoriteMusic",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "music",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="favorite_musics",
                        to="music.music",
                        verbose_name="music",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="favorite_musics",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="user",
                    ),
                ),
            ],
        ),
    ]
