from django.contrib import admin

from subscription.models import Subscription, SubscriptionDetail

admin.site.register(Subscription)
admin.site.register(SubscriptionDetail)
