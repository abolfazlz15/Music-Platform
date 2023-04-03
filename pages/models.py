from django.db import models

from accounts.models import User
from utils.date_conversion.utils import jajali_converter


class ContactUsTitle(models.Model):
    title = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'عنوان تیکت'
        verbose_name_plural = 'عنواین تیکت'

    def __str__(self):
        return self.title


class Ticket(models.Model):
    title = models.ForeignKey(ContactUsTitle, related_name='tickets', null=True, on_delete=models.SET_NULL)
    body = models.TextField()
    user = models.ForeignKey(User, related_name='tickets', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'تیکت'
        verbose_name_plural = 'تیکت'

    def __str__(self):
        return f'{self.title} - {self.body[:10]}'

    def get_jalali_date(self):
        return jajali_converter(self.created_at)
    get_jalali_date.short_description = 'تاریخ ثبت'