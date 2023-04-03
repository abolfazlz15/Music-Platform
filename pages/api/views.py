from rest_framework import generics

from pages.api import serializers
from pages.models import Ticket


# Tecket APIs 
class CreateTicketView(generics.CreateAPIView):
    queryset = Ticket
    serializer_class = serializers.ContactUsSerializer
    