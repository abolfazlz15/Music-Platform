from django.db import models
from django.db.models.functions import Lower
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from pages.api import serializers
from pages.models import Ticket, TicketTitle


# Tecket APIs 
class CreateTicketView(generics.CreateAPIView):
    queryset = Ticket
    serializer_class = serializers.TicketSerializer
    

class TicketTitleListView(generics.GenericAPIView):
    def get(self, request):
        try:
            queryset = TicketTitle.objects.all().exclude(title='دیگر')
            third_object = TicketTitle.objects.get(title='دیگر')
            all_objects = list(queryset) + [third_object]
            serializer = serializers.TicketTitleListSerializer(instance=all_objects, many=True)
        except:
            queryset = TicketTitle.objects.all()
            serializer = serializers.TicketTitleListSerializer(instance=queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)