from django.db.models import Count
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from music.models import Music
from play_list.api import permissions as custom_permissions
from play_list.api import serializers
from play_list.models import Playlist, ApprovedPlaylist


class UserPlayListView(APIView):
    serializer_class = serializers.PlayListSerializer

    def get(self, request, pk):
        queryset = Playlist.objects.select_related('user').filter(user__id=pk).annotate(number_of_songs=Count('songs')).order_by('-id')
        serializer = self.serializer_class(instance=queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailPlayListView(APIView):
    serializer_class = serializers.PlayListDetailSerializer

    def get(self, request, pk):
        queryset = Playlist.objects.prefetch_related('songs__artist').get(id=pk)
        serializer = self.serializer_class(instance=queryset, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserCreatePlayListView(APIView):
    serializer_class = serializers.PlayListUpdateAndCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['user'] = request.user
            serializer.save()
            return Response({'result': 'playlist created', 'success': True}, status=status.HTTP_201_CREATED)
        return Response({'result': serializer.errors, 'success': True}, status=status.HTTP_400_BAD_REQUEST)


class UserUpdatePlayListView(APIView):
    serializer_class = serializers.PlayListUpdateAndCreateSerializer
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
        return Response({'success': True, 'message': 'playlist deleted'}, status=status.HTTP_204_NO_CONTENT)


class PlaylistAddMusicView(generics.UpdateAPIView):
    serializer_class = serializers.PlaylistAddAndRemoveSerializer
    permission_classes = [custom_permissions.IsAuthorOrReadOnly]

    def put(self, request, pk, *args, **kwargs):
        try:
            playlist = Playlist.objects.get(user=request.user, id=pk)
        except Playlist.DoesNotExist:
            return Response({'message': 'Invalid playlist ID', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        music_id = request.data.get('music_id')

        self.check_object_permissions(self.request, playlist)
        try:
            music = Music.objects.get(id=music_id)
        except Music.DoesNotExist:
            return Response({'message': 'Invalid music ID', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        playlist.songs.add(music)

        serializer = self.get_serializer(playlist)
        return Response({'result': 'music added', 'data': serializer.data, 'success': True}, status=status.HTTP_200_OK)


class PlaylistRemoveMusicView(generics.DestroyAPIView):
    serializer_class = serializers.PlaylistAddAndRemoveSerializer
    permission_classes = [custom_permissions.IsAuthorOrReadOnly]

    def delete(self, request, pk):
        try:
            playlist = Playlist.objects.get(user=request.user, id=pk)

        except Playlist.DoesNotExist:
            return Response({'message': 'Invalid playlist ID', 'success': False}, status=status.HTTP_400_BAD_REQUEST)

        music_id = request.data.get('music_id')
        self.check_object_permissions(self.request, playlist)
        try:
            music = playlist.songs.get(id=music_id)
        except Music.DoesNotExist:
            return Response({'message': 'Invalid music ID', 'success': False}, status=status.HTTP_400_BAD_REQUEST)
        playlist.songs.remove(music)

        serializer = self.get_serializer(playlist)
        return Response({'result': 'music remove', 'data': serializer.data, 'success': True},
                        status=status.HTTP_204_NO_CONTENT)


class ApprovedPlaylistView(APIView):
    
    def get(self, request):
        international_playlist = ApprovedPlaylist.objects.filter(is_international=True)[:5]
        iranian_playlist = ApprovedPlaylist.objects.filter(is_international=False)[:5]
        iranian_playlist_serializer = serializers.ApprovedPlaylistSerializer(iranian_playlist, many=True, context={'request': request})
        international_playlist_serializer = serializers.ApprovedPlaylistSerializer(international_playlist, many=True, context={'request': request})

        queryset = {
            'international_playlist': international_playlist_serializer.data,
            'iranian_playlist': iranian_playlist_serializer.data,
        }
        return Response(queryset)


class ApprovedPlaylistDetailView(APIView):
    serializer_class = serializers.ApprovedPlaylistDetailSerializer

    def get(self, request, pk):
        queryset = ApprovedPlaylist.objects.prefetch_related('songs__artist').get(id=pk)
        serializer = self.serializer_class(instance=queryset, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)