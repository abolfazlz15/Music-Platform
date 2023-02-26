from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from play_list.api import serializers
from play_list.models import Playlist


class UserPlayListView(APIView):
    serializer_class = serializers.PlayListSerializer

    def get(self, request, pk):
        queryset = Playlist.objects.filter(user__id=pk)
        serializer = self.serializer_class(instance=queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailPlayListView(APIView):
    serializer_class = serializers.PlayListDetailSerializer
    
    def get(self, request, pk):
        queryset = Playlist.objects.get(id=pk)
        serializer = self.serializer_class(instance=queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCreatePlayListView(APIView):
    serializer_class = serializers.PlayListCreateSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response({'result': 'playlist created'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)