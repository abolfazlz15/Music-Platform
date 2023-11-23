from django.db import models

from accounts.models import User

class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    count_of_sub = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username
    