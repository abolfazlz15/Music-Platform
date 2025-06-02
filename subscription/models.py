from django.db import models

from accounts.models import User


class Subscription(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


class SubscriptionDetail(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="subscription"
    )
    subscription_plan = models.ForeignKey(
        Subscription, on_delete=models.CASCADE, related_name="plans"
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    expire_at = models.DateTimeField(editable=False, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
