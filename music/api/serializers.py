from rest_framework import serializers

from music.models import Music

class ArticleListSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Music
        fields = ('id', 'title', 'artist', 'cover')


