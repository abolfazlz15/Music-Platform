from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from accounts.forms import UserChangeForm, UserCreationForm
from accounts.models import Artist, ImageProfile, User
from django.utils.translation import gettext_lazy as _


admin.site.site_header = _("Music Platform")
admin.site.site_title = _("Music Platform")
admin.site.index_title = _("Music Platform Management")


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances

    form = UserChangeForm
    add_form = UserCreationForm

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == "is_superuser" and not request.user.is_superuser:
            field.widget = forms.HiddenInput()
        return field

    def has_delete_permission(self, request, obj=None):
        if obj is not None and request.user.is_superuser == False:
            if request.user.is_admin and obj.is_admin:
                return False
            else:
                return True
        else:
            return True

    def has_change_permission(self, request, obj=None):
        if obj is not None and request.user.is_superuser == False:
            if request.user.is_admin and request.user.email == obj.email:
                return True
            elif request.user.is_admin and obj.is_admin:
                return False
            else:
                return True
        else:
            return True

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        if not request.user.is_superuser:
            return (
                (None, {"fields": ("email", "password")}),
                (
                    "Personal info",
                    {"fields": ("username", "profile_image", "get_jalali_date")},
                ),
                ("Permissions", {"fields": ("is_active",)}),
            )
        return super().get_fieldsets(request, obj)

    list_display = ("email", "username", "is_admin", "is_active", "get_jalali_date")
    list_filter = ("is_admin", "is_active", "is_superuser")

    fieldsets = [
        (None, {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["username", "profile_image", "get_jalali_date"]}),
        ("Permissions", {"fields": ["is_admin", "is_superuser", "is_active"]}),
    ]

    readonly_fields = ("get_jalali_date",)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email", "username")
    ordering = ("email",)
    filter_horizontal = ()
    list_select_related = ["profile_image"]
    list_per_page = 50


admin.site.register(User, UserAdmin)
admin.site.register(ImageProfile)
admin.site.register(Artist)

admin.site.unregister(Group)
