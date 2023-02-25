from rest_framework.views import APIView
from rest_framework.response import Response

from play_list.api import serializers
from play_list.models import Playlist


class UserPlayListView(APIView):
    serializer_class = serializers.PlayListSerializer

    def get(self, request, pk):
        queryset = Playlist.objects.filter(user__id=pk)
        serializer = self.serializer_class(instance=queryset, many=True)
        return Response(serializer.data)
