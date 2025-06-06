from django.contrib import admin, messages
from django.utils.translation import ngettext

from music import models

admin.site.register(models.FavoriteMusic)
admin.site.register(models.ChooseMusicByCategory)
admin.site.register(models.HomeSlider)
admin.site.register(models.IPAddress)


@admin.register(models.Music)
class MusicAdmin(admin.ModelAdmin):
    # for show customization list objects
    fields = (
        "title",
        "artist",
        "cover",
        "text",
        "category",
        "type",
        "status",
        "url",
        "music_file",
        "views",
        "created_at",
    )
    list_display = ("show_cover", "title", "get_artist", "status", "category")
    list_filter = ("status", "type", "created_at")
    search_fields = ("title", "created_at", "artist__name")
    ordering = ("status",)
    readonly_fields = ("created_at",)
    autocomplete_fields = ["category"]
    list_display_links = (
        "title",
        "show_cover",
    )
    actions = ["make_published", "make_depublish"]
    list_select_related = ["category"]
    filter_horizontal = ["artist"]
    list_per_page = 50

    def get_artist(self, obj):
        return "\n ,".join([p.name for p in obj.artist.all()])

    @admin.action(description="Mark selected musics as published")
    def make_published(self, request, queryset):
        updated = queryset.update(status=True)
        self.message_user(
            request,
            ngettext(
                "%d music was successfully marked as published.",
                "%d musics were successfully marked as published.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )

    @admin.action(description="Mark selected musics as hide")
    def make_depublish(self, request, queryset):
        updated = queryset.update(status=False)
        self.message_user(
            request,
            ngettext(
                "%d music was successfully marked as hide.",
                "%d musics were successfully marked as hide.",
                updated,
            )
            % updated,
            messages.SUCCESS,
        )


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    # for show customization list objects
    fields = ("title", "image")
    list_display = ("show_cover", "title")
    search_fields = ("title",)

    list_display_links = ("show_cover", "title")
