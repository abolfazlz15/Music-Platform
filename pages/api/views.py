from rest_framework import generics, status
from rest_framework.response import Response

from pages.api import serializers
from pages.models import AboutUs, Ticket, TicketTitle


# Ticket APIs
from rest_framework import status
from rest_framework.response import Response

class CreateTicketView(generics.CreateAPIView):
    queryset = Ticket
    serializer_class = serializers.TicketSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'success': True, 'message': 'Ticket created successfully'}, status=status.HTTP_201_CREATED, headers=headers)


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


# AboutUs API
class AboutUsView(generics.GenericAPIView):
    def get(self, request):
        queryset = AboutUs.objects.first()
        serializer = serializers.AboutUsSerializer(instance=queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
