# Generated by Django 4.1.6 on 2023-03-14 16:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_user_register_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='artist',
            options={'verbose_name': 'هنرمتد', 'verbose_name_plural': 'هنرمندان'},
        ),
        migrations.AlterModelOptions(
            name='imageprofile',
            options={'verbose_name': 'عکس پروفایل', 'verbose_name_plural': 'عکس پروفایل ها'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'کاربر', 'verbose_name_plural': 'کاربران'},
        ),
    ]
