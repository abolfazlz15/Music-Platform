from rest_framework import serializers

from subscription.models import Subscription


class MemberShipListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"
