from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from music.models import Music
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
    permission_classes = [custom_permissions.IsAuthorOrReadOnly]

    def delete(self, request, pk):
        playlist = get_object_or_404(Playlist, id=pk)
        self.check_object_permissions(request, playlist)

        playlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PlaylistAddMusicView(generics.UpdateAPIView):
    serializer_class = serializers.PlayListSerializer
    permission_classes = [custom_permissions.IsAuthorOrReadOnly]

    def put(self, request, pk, *args, **kwargs):
        try:
            playlist = Playlist.objects.get(user=request.user, id=pk)
        except Playlist.DoesNotExist:
            return Response({'message': 'Invalid playlist ID'}, status=status.HTTP_400_BAD_REQUEST)

        music_id = request.data.get('music_id')
        self.check_object_permissions(self.request, playlist)
        try:
            music = Music.objects.get(id=music_id)
        except Music.DoesNotExist:
            return Response({'message': 'Invalid music ID'}, status=status.HTTP_400_BAD_REQUEST)

        playlist.songs.add(music)

        serializer = self.get_serializer(playlist)
        return Response({'result': 'music added', 'data': serializer.data}, status=status.HTTP_200_OK)
    

class PlaylistRemoveMusicView(generics.DestroyAPIView):
    serializer_class = serializers.PlayListSerializer
    permission_classes = [custom_permissions.IsAuthorOrReadOnly]

    def delete(self, request, pk):
        try:
            playlist = Playlist.objects.get(user=request.user, id=pk)
            
        except Playlist.DoesNotExist:
            return Response({'message': 'Invalid playlist ID'}, status=status.HTTP_400_BAD_REQUEST)

        music_id = request.data.get('music_id')
        self.check_object_permissions(self.request, playlist)
        try:
            music = playlist.songs.get(id=music_id)
        except Music.DoesNotExist:
            return Response({'message': 'Invalid music ID'}, status=status.HTTP_400_BAD_REQUEST)
        playlist.songs.remove(music)

        serializer = self.get_serializer(playlist)
        return Response({'result': 'music remove', 'data': serializer.data}, status=status.HTTP_204_NO_CONTENT)

