from rest_framework import serializers

from accounts.models import Artist, User
from music.models import Category, HomeSlider, Music
from play_list.models import Playlist

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')




class PlayListSerializer(serializers.ModelSerializer):
    # user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Playlist
        fields = ('id', 'name', 'user')

    def get_user(self, obj):
        serializer = UserSerializer(instance=obj.user)
        return serializer.data

# class MusicDetailSerializer(serializers.ModelSerializer):
#     artist = serializers.SerializerMethodField()
#     category = serializers.SerializerMethodField()

#     class Meta:
#         model = Music
#         fields = ('id', 'title', 'artist', 'cover', 'text', 'category')

#     def get_artist(self, obj):
#         serializer = ArtistSerializer(instance=obj.artist.all(), many=True)
#         return serializer.data

#     def get_category(self, obj):
#         serializer = CategorySerializer(instance=obj.category.all(), many=True)
#         return serializer.data


# class SliderHomePageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = HomeSlider
#         fields = '__all__'


# class CategoryListSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = '__all__'
