# Generated by Django 4.1.6 on 2023-03-14 16:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("music", "0007_alter_category_options_alter_music_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="choosemusicbycategory",
            options={
                "verbose_name": "نمایش موزیک بر اساس دسته بندی در صفحه خانه",
                "verbose_name_plural": "نمایش موزیک بر اساس دسته بندی در صفحه خانه",
            },
        ),
        migrations.AlterModelOptions(
            name="favoritemusic",
            options={
                "verbose_name": "موزیک لایک شده کاربر",
                "verbose_name_plural": "موزیک های لایک شده کاربر",
            },
        ),
        migrations.AlterModelOptions(
            name="homeslider",
            options={
                "verbose_name": "اسلایدر صفحه خانه",
                "verbose_name_plural": "اسلایدر های صفحه خانه",
            },
        ),
        migrations.AlterField(
            model_name="category",
            name="image",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to="image/category_image",
                verbose_name="image",
            ),
        ),
    ]
