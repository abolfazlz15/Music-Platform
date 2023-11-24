from datetime import timedelta

from django.db.models.signals import post_save
from django.dispatch import receiver

from subscription.models import SubscriptionDetail


@receiver(post_save, sender=SubscriptionDetail)
def set_subscription_expire_time(sender, instance, created, *args, **kwargs):
    """
    set subscription expire time
    """
    if created:
        expire_time = instance.created_at + timedelta(days=30)
        instance.expire_at = expire_time
        instance.save()


