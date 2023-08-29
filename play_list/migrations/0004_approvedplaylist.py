# Generated by Django 4.1.6 on 2023-08-29 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0011_alter_music_category'),
        ('play_list', '0003_alter_playlist_songs'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovedPlaylist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='name')),
                ('cover', models.ImageField(upload_to='image/palylist/cover')),
                ('is_international', models.BooleanField(default=False)),
                ('songs', models.ManyToManyField(blank=True, related_name='approved_playlists', to='music.music', verbose_name='songs')),
            ],
            options={
                'verbose_name': 'پلی لیست عمومی',
                'verbose_name_plural': 'پلی لیست های عمومی',
            },
        ),
    ]
