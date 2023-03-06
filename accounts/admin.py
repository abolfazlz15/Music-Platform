from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from accounts.forms import UserChangeForm, UserCreationForm
from accounts.models import Artist, ImageProfile, User


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances

    form = UserChangeForm
    add_form = UserCreationForm

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        field = super().formfield_for_dbfield(db_field, request, **kwargs)
        if db_field.name == 'is_superuser' and not request.user.is_superuser:
            field.widget = forms.HiddenInput()
        return field
    
    def get_form(self, request, obj=None, **kwargs):
        obj = super().get_form(request, obj, **kwargs)
        
        is_superuser = request.user.is_superuser
        if not is_superuser:
            obj.base_fields['is_admin'].disabled = True


        elif obj and not obj.is_superuser :
            obj.base_fields['is_active'].disabled = True
            obj.base_fields['is_active'].help_text = "You do not have permission to change this field for other admins."    
        return obj

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