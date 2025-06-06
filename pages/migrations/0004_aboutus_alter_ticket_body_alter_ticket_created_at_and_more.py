# Generated by Django 4.1.6 on 2023-04-13 08:05

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("pages", "0003_rename_contactustitle_tickettitle_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="AboutUs",
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
                ("version", models.CharField(max_length=100, verbose_name="version")),
                (
                    "description",
                    ckeditor.fields.RichTextField(
                        blank=True, null=True, verbose_name="description"
                    ),
                ),
            ],
            options={
                "verbose_name": "درباره ما",
                "verbose_name_plural": "درباره ما",
            },
        ),
        migrations.AlterField(
            model_name="ticket",
            name="body",
            field=models.TextField(verbose_name="body"),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, verbose_name="created at"),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="title",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="tickets",
                to="pages.tickettitle",
                verbose_name="title",
            ),
        ),
        migrations.AlterField(
            model_name="ticket",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to=settings.AUTH_USER_MODEL,
                verbose_name="user",
            ),
        ),
        migrations.AlterField(
            model_name="tickettitle",
            name="title",
            field=models.CharField(max_length=200, verbose_name="title"),
        ),
    ]
