from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from settings.api.serializers import SettingDetailSerializer
from settings.models import Settings


class SettingDetailView(GenericAPIView):
    serializer_class = SettingDetailSerializer
    def get(self, request):
        try:
            settings = Settings.objects.last()
            return Response(
                data=self.serializer_class(instance=settings).data,
                status=status.HTTP_200_OK
            )
        except Settings.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)