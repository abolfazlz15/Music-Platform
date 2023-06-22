from rest_framework import serializers

from accounts.models import User
from music.api.serializers import MusicListSerializer
from play_list.models import Playlist


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')


class PlayListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Playlist
        fields = ('id', 'name', 'user')

    def get_user(self, obj):
        serializer = UserSerializer(instance=obj.user)
        return serializer.data


class PlayListDetailSerializer(serializers.ModelSerializer):
    music = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ('id', 'name', 'music')

    def get_music(self, obj):
        request = self.context.get('request')
        serializer = MusicListSerializer(instance=obj.songs.all(), many=True, context={'request': request})
        return serializer.data


class PlayListCreateSerializer(serializers.ModelSerializer):
    user = serializers.CharField(required=False)

    class Meta:
        model = Playlist
        fields = ('name', 'user')
