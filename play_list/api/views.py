from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from play_list.api import permissions as custom_permissions
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
    

class UserUpdatePlayListView(APIView):
    serializer_class = serializers.PlayListCreateSerializer
    permission_classes = [custom_permissions.IsAuthorOrReadOnly]
    
    def put(self, request, pk):
        instance = Playlist.objects.get(id=pk)
        self.check_object_permissions(request, instance)
        serializer = self.serializer_class(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'result': 'playlist updated'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeletePlayListView(APIView):

    def delete(self, request, pk):
        self.permission_classes = [custom_permissions.IsAuthorOrReadOnly]
        playlist = get_object_or_404(Playlist, id=pk)
        self.check_object_permissions(request, playlist)

        playlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

