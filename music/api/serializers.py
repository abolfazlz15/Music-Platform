from rest_framework import serializers

from music.models import Music, HomeSlider
from accounts.models import Artist


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name')


class MusicListSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Music
        fields = ('id', 'title', 'artist', 'cover')


class MusicDetailSerializer(serializers.ModelSerializer):
    artist = serializers.SerializerMethodField()

    class Meta:
        model = Music
        fields = ('id', 'title', 'artist', 'cover')

    def get_artist(self, obj):
        serializer = ArtistSerializer(instance=obj.artist.all(), many=True)
        return serializer.data


class SliderHomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSlider
        fields = '__all__'
