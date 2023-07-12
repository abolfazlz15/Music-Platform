from django.contrib import admin
from play_list.models import Playlist

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    # for show customization list objects
    fields = ('name', 'user', 'songs', 'approved_playlist')
    list_display = ('name', 'user', 'approved_playlist')
    search_fields = ('user', 'name')
    filter_horizontal = ['songs']
    list_select_related = ['user']
    list_per_page = 50
    list_filter = ['approved_playlist']