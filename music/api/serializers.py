from django.utils.html import strip_tags
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from accounts.models import Artist
from music.models import Category, HomeSlider, Music


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ("id", "name", "image")


class MusicByCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.StringRelatedField(source="category")
    artist = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = Music
        fields = ("id", "title", "artist", "cover", "category_name")

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        category_name = self.context.get("category_name")
        representation["category_name"] = category_name
        return representation


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "title")


class MusicListSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")
    cover = serializers.SerializerMethodField()

    class Meta:
        model = Music
        fields = ("id", "title", "artist", "cover")

    def get_cover(self, obj) -> None | str:
        request = self.context.get("request")
        # add base URL for cover music
        if obj.cover:
            image_url = obj.cover.url
            return request.build_absolute_uri(image_url)
        return None


class MusicDetailSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer(many=True)
    category = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()
    like = serializers.SerializerMethodField()
    related_music = serializers.SerializerMethodField()

    class Meta:
        model = Music
        fields = (
            "id",
            "title",
            "artist",
            "cover",
            "text",
            "url",
            "music_file",
            "category",
            "like",
            "related_music",
        )

    @extend_schema_field(CategorySerializer)
    def get_category(self, obj):
        return CategorySerializer(instance=obj.category)

    def get_cover(self, obj) -> None | str:
        request = self.context.get("request")
        # add base URL for cover music
        if obj.cover:
            image_url = obj.cover.url
            return request.build_absolute_uri(image_url)
        return None

    def get_like(self, obj) -> bool:
        return self.context.get("is_liked")

    @extend_schema_field(MusicListSerializer(many=True))
    def get_related_music(self, obj):
        context = self.context.get("related_music")
        return MusicListSerializer(
            instance=context,
            many=True,
            context={"request": self.context.get("request")},
        ).data

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        skip_music = self.context.get("skip_music")
        representation["skip_music"] = skip_music
        representation["text"] = strip_tags(instance.text)

        return representation


class SliderHomePageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeSlider
        fields = "__all__"


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
