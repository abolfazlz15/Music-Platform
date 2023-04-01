from django.db import models
from utils.date_conversion.utils import jajali_converter


class ContactUsTitle(models.Model):
    title = models.CharField(max_length=200)


class ContactUs(models.Model):
    title = models.ForeignKey(ContactUsTitle, related_name='contacts', null=True, on_delete=models.SET_NULL)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} - {self.body[:10]}'

    def get_jalali_date(self):
        return jajali_converter(self.created_at)
    get_jalali_date.short_description = 'تاریخ ثبت'