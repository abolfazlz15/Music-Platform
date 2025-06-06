# Generated by Django 4.1.6 on 2023-02-13 18:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_imageprofile_user_profile_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="Artist",
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
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="artist_profile/"
                    ),
                ),
                ("name", models.CharField(max_length=50)),
            ],
        ),
    ]
