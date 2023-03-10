from django.contrib import admin
from play_list.models import Playlist

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    # for show customization list objects
    fields = ('name', 'user', 'songs')
    list_display = ('name', 'user')
    search_fields = ('user', 'name')

    list_display = ('name', 'user')