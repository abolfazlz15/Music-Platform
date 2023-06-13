# Generated by Django 4.1.6 on 2023-06-10 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0010_remove_music_category_music_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='music',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='musics', to='music.category', verbose_name='category'),
            preserve_default=False,
        ),
    ]