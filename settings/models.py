from django.db import models

class Settings(models.Model):
    is_new_update = models.BooleanField(default=False, blank=True, null=True)
    is_update_required = models.BooleanField(default=False, blank=True, null=True)
    

