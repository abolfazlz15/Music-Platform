# Generated by Django 4.1.6 on 2023-07-12 17:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('play_list', '0003_alter_playlist_songs'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='approved_playlist',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='playlist',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='playlists', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
