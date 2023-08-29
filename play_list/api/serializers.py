from rest_framework import serializers

from accounts.models import User
from music.api.serializers import MusicListSerializer
from play_list.models import Playlist, ApprovedPlaylist


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class PlayListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True, required=False)
    cover = serializers.SerializerMethodField(read_only=True)
    number_of_songs = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Playlist
        fields = ('id', 'name', 'user', 'cover', 'number_of_songs')

    def get_user(self, obj):
        serializer = UserSerializer(instance=obj.user)
        return serializer.data
    
    def get_cover(self, obj):
        request = self.context.get('request')
        music = obj.songs.first() 
        if music:
            cover = music.cover.url
            return request.build_absolute_uri(cover)
        return None

    def get_number_of_songs(self, obj):
        return obj.number_of_songs


class PlayListDetailSerializer(serializers.ModelSerializer):
    music = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ('id', 'name', 'music')

    def get_music(self, obj):
        request = self.context.get('request')
        serializer = MusicListSerializer(instance=obj.songs.all(), many=True, context={'request': request})
        return serializer.data


class PlayListUpdateAndCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)

    class Meta:
        model = Playlist
        fields = ('name', 'user')


class PlaylistAddAndRemoveSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Playlist
        fields = ('id', 'name', 'user')


class ApprovedPlaylistSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApprovedPlaylist
        fields = ('id', 'name', 'cover')