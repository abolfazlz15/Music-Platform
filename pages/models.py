from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _

from accounts.models import User
from utils.date_conversion.utils import jajali_converter


class TicketTitle(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('title'))

    class Meta:
        verbose_name = 'عنوان تیکت'
        verbose_name_plural = 'عنواین تیکت'

    def __str__(self):
        return self.title


class Ticket(models.Model):
    title = models.ForeignKey(TicketTitle, related_name='tickets', null=True, on_delete=models.SET_NULL, verbose_name=_('title'))
    body = models.TextField(verbose_name=_('body'))
    user = models.ForeignKey(User, related_name='tickets', on_delete=models.CASCADE, verbose_name=_('user'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created at'))

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت'

    def __str__(self):
        return f'{self.title} - {self.body[:10]}'

    def get_jalali_date(self):
        return jajali_converter(self.created_at)
    get_jalali_date.short_description = 'تاریخ ثبت'


class AboutUs(models.Model):
    version = models.CharField(max_length=100, verbose_name=_('version'))
    description = RichTextField(verbose_name=_('description'), null=True, blank=True)

    class Meta:
        verbose_name = 'درباره ما'
        verbose_name_plural = 'درباره ما'

    def __str__(self):
        return f'{self.version} - {self.description[:10]}'    