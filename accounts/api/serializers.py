from django.contrib.auth import authenticate, password_validation
from django.db.models import Count
from rest_framework import serializers, status
from rest_framework.exceptions import ParseError
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema_field

from accounts.models import Artist, ImageProfile, User
from music.api.serializers import MusicListSerializer


class ImageProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProfile
        fields = ("image",)

    # def get_image(self, obj):
    #     request = self.context.get('request')
    #     # add base URL for cover music
    #     if obj.image:
    #         image_url = obj.image.url
    #         return request.build_absolute_uri(image_url)
    #     return None


class UserDetailSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, obj) -> None | str:
        request = self.context.get("request")
        if obj.profile_image:
            image_url = obj.profile_image.image.url
            return request.build_absolute_uri(image_url)
        return None

    class Meta:
        model = User
        fields = ("id", "email", "username", "image")


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ("profile_image", "username")

    def validate_username(self, value):
        user = User.objects.filter(username=value)
        if user:
            raise ParseError(
                {"error": "username already exists"}, code=status.HTTP_400_BAD_REQUEST
            )
        else:
            return value


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False)

    def validate(self, attrs):
        user = authenticate(**attrs)

        if user:
            return user
        raise ParseError(
            {"error": "user doesn't exist"}, code=status.HTTP_400_BAD_REQUEST
        )

    def save(self, validated_data):
        refresh = RefreshToken.for_user(validated_data)
        return {
            "username": validated_data.username,
            "user_id": validated_data.id,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "password")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate_password(self, value):
        try:
            password_validation.validate_password(value, self.instance)
        except serializers.ValidationError as error:
            self.add_error("password", error)
        return value


class GetOTPRegisterCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)
    email = serializers.EmailField()

    def save(self, validated_data):
        refresh = RefreshToken.for_user(validated_data)
        return {
            "user_id": validated_data.id,
            "success": True,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=False)
    new_password = serializers.CharField(required=False)

    def validate_new_password(self, value):
        try:
            password_validation.validate_password(value, self.instance)
        except serializers.ValidationError as error:
            self.add_error("password", error)
        return value


class ArtistDetailSerializer(serializers.ModelSerializer):
    music_quantity = serializers.SerializerMethodField()
    recent_music = serializers.SerializerMethodField()
    popular_music = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = (
            "id",
            "name",
            "image",
            "music_quantity",
            "recent_music",
            "popular_music",
        )

    def get_music_quantity(self, artist) -> int:
        return artist.musics.count()

    @extend_schema_field(MusicListSerializer(many=True))
    def get_recent_music(self, artist):
        request = self.context.get("request")
        musics = artist.musics.order_by("-created_at")[:10]
        return MusicListSerializer(musics, many=True, context={"request": request}).data

    @extend_schema_field(MusicListSerializer(many=True))
    def get_popular_music(self, artist):
        """
        Retrieve 10 most popular music tracks
        """
        request = self.context.get("request")
        musics = (
            artist.musics.annotate(play_count=Count("favorite_musics"))
            .filter(status=True)
            .order_by("-play_count")[:10]
        )
        return MusicListSerializer(musics, many=True, context={"request": request}).data

    def get_image(self, obj) -> None | str:
        request = self.context.get("request")
        # add base URL for cover music
        if obj.image:
            image_url = obj.image.url
            return request.build_absolute_uri(image_url)
        return None


class ArtistListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ("id", "name", "image")

    def get_image(self, obj) -> None | str:
        request = self.context.get("request")
        # add base URL for cover music
        if obj.image:
            image_url = obj.image.url
            return request.build_absolute_uri(image_url)
        return None


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ImageListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProfile
        fields = "__all__"
