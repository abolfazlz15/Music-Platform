from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from accounts.managers import UserManager
from utils.date_conversion.utils import jajali_converter

class ImageProfile(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('title'))
    image = models.ImageField(upload_to='profile_image', verbose_name=_('image profile'))   
    
    class Meta:
        verbose_name = 'عکس پروفایل'
        verbose_name_plural = 'عکس پروفایل ها'

    def __str__(self):
        return self.title


class User(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(
        verbose_name=_('email address'),
        max_length=255,
        unique=True,
    )
    username = models.CharField(unique=True, max_length=100, verbose_name=_('username'))
    profile_image = models.ForeignKey(ImageProfile, null=True, blank=True, on_delete=models.SET_NULL, related_name='users', verbose_name=_('image/profile_image'))
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    register_at = models.DateTimeField(auto_now_add=True, null=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        # Simplest possible answer: Yes, always
        return True
    
    def get_jalali_date(self):
        return jajali_converter(self.register_at)
    get_jalali_date.short_description = 'تاریخ عضویت'

    @property
    def is_staff(self):
        # Simplest possible answer: All admins are staff
        return self.is_admin


class Artist(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='artist_profile/', null=True, blank=True)
    class Meta:
        verbose_name = 'هنرمتد'
        verbose_name_plural = 'هنرمندان'
        
    def __str__(self):
        return self.name
