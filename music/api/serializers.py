from rest_framework import serializers

from music.models import Music, HomeSlider



class MusicListSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Music
        fields = ('id', 'title', 'artist', 'cover')


class SliderHomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSlider
        fields = '__all__'
