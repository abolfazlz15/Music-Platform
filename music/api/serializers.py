from rest_framework import serializers

from accounts.models import Artist
from music.models import Category, HomeSlider, Music


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ('id', 'name')


class MusicByCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source='category')
    artist = serializers.SlugRelatedField(slug_field='name', read_only=True)

    
    class Meta:
        model = Music
        fields = ('id', 'title', 'artist', 'cover', 'category_name')
        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        category_name = self.context.get('category_name')
        representation['category_name'] = category_name
        return representation


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'title')


class MusicListSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(many=True, read_only=True, slug_field='name')
    class Meta:
        model = Music
        fields = ('id', 'title', 'artist', 'cover')


class MusicDetailSerializer(serializers.ModelSerializer):
    artist = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    class Meta:
        model = Music
        fields = ('id', 'title', 'artist', 'cover', 'text', 'category')

    def get_artist(self, obj):
        serializer = ArtistSerializer(instance=obj.artist.all(), many=True)
        return serializer.data

    def get_category(self, obj):
        serializer = CategorySerializer(instance=obj.category.all(), many=True)
        return serializer.data


class SliderHomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSlider
        fields = '__all__'


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
