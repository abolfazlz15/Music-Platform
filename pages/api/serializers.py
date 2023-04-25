from rest_framework import serializers

from pages.models import Ticket, TicketTitle, AboutUs


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

        