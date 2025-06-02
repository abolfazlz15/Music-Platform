from rest_framework import generics

from subscription.api import serializers
from subscription.models import Subscription


class MemberShipListView(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = serializers.MemberShipListSerializer
