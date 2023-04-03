from rest_framework import serializers
from pages.models import Ticket

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('user', 'body', 'title')

