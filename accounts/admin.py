from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from accounts.forms import UserChangeForm, UserCreationForm
from accounts.models import User, ImageProfile, Artist

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm


    list_display = ('email', 'username', 'is_admin', 'is_active', 'get_jalali_date')
    list_filter = ('is_admin', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'profile_image', 'get_jalali_date')}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'is_superuser')}),
    )
    readonly_fields = ('get_jalali_date',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    filter_horizontal = ()




admin.site.register(User, UserAdmin)
admin.site.register(ImageProfile)


admin.site.register(Artist)

admin.site.unregister(Group)