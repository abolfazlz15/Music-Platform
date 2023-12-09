from rest_framework import serializers

from pages.models import Ticket, TicketTitle, AboutUs
from django.utils.html import strip_tags


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('user', 'body', 'title')

class TicketTitleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketTitle
        fields = '__all__'


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)


        representation['description'] = strip_tags(instance.description)

        return representation
        