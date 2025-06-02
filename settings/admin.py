from django.contrib import admin
from settings.models import Settings


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ("id", "is_new_update", "is_update_required")
