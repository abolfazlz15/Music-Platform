from celery import shared_task
from django.utils import timezone

from subscription.models import SubscriptionDetail


@shared_task
def deactivate_expired_subscription():
    current_datetime = timezone.now()
    expired_subscriptions = SubscriptionDetail.objects.filter(expire_at__lt=current_datetime)

    for subscription in expired_subscriptions:
        subscription.is_active = False
        subscription.save()