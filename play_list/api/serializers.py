from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from accounts.models import User
from music.api.serializers import MusicListSerializer
from play_list.models import ApprovedPlaylist, Playlist


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

    @extend_schema_field(UserSerializer)
    def get_user(self, obj):
        return UserSerializer(instance=obj.user)
    
    def get_cover(self, obj) -> None | str:
        request = self.context.get('request')
        music = obj.songs.last()
        if music:
            cover = music.cover.url
            return request.build_absolute_uri(cover)
        return None

    def get_number_of_songs(self, obj) -> int:
        return obj.number_of_songs


class PlayListDetailSerializer(serializers.ModelSerializer):
    music = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ('id', 'name', 'music')

    @extend_schema_field(MusicListSerializer(many=True))
    def get_music(self, obj):
        request = self.context.get('request')
        return MusicListSerializer(instance=obj.songs.all(), many=True, context={'request': request}).data


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

    def get_cover(self, obj) -> None | str:
        request = self.context.get('request')
        music = obj.songs.first() 
        if music:
            cover = music.cover.url
            return request.build_absolute_uri(cover)
        return None

class ApprovedPlaylistDetailSerializer(serializers.ModelSerializer):
    music = serializers.SerializerMethodField()

    class Meta:
        model = ApprovedPlaylist
        fields = ('id', 'name' , 'cover', 'music')

    @extend_schema_field(MusicListSerializer(many=True))
    def get_music(self, obj):
        request = self.context.get('request')
        return MusicListSerializer(instance=obj.songs.all(), many=True, context={'request': request}).data