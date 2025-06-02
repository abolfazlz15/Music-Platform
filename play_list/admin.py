from django.contrib import admin

from play_list.models import ApprovedPlaylist, Playlist


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    fields = ("name", "user", "songs")
    list_display = ("name", "user")
    search_fields = ("user", "name")
    filter_horizontal = ["songs"]
    list_select_related = ["user"]
    list_per_page = 50


@admin.register(ApprovedPlaylist)
class ApprovedPlaylistAdmin(admin.ModelAdmin):
    fields = ("name", "songs", "is_international", "cover")
    list_display = ("name", "is_international")
    search_fields = ("name",)
    filter_horizontal = ["songs"]
    list_per_page = 50
    list_filter = ["is_international"]
