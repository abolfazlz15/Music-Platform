from django.contrib import admin

from music import models

admin.site.register(models.Music)
admin.site.register(models.Category)
admin.site.register(models.FavoriteMusic)
admin.site.register(models.ChooseMusicByCategory)
admin.site.register(models.HomeSlider)