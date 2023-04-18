from django.contrib.auth import authenticate, password_validation
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password

from accounts.models import Artist, ImageProfile, User
from music.api.serializers import MusicListSerializer
from django.db.models import Count

class ImageProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProfile
        fields = ('image',)


class UserSerializer(serializers.ModelSerializer):
    profile_image = ImageProfileSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'profile_image')


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ('profile_image', 'username')

    def validate_username(self, value):
        user = User.objects.filter(username=value)
        if user:
            raise serializers.ValidationError({'error': 'this username exist'})
        else:
            return value


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    password = serializers.CharField(required=False)

    def validate(self, attrs):
        user = authenticate(**attrs)

        if user:
            return user
        raise serializers.ValidationError({'error': 'this user is not exist', 'success': False})

    def save(self, validated_data):
        refresh = RefreshToken.for_user(validated_data)
        return ({
            'user_id': validated_data.id,
            'success': True,
            'refresh': str(refresh),
            'access': str(refresh.access_token),

        })


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        try:
            password_validation.validate_password(value, self.instance)
        except serializers.ValidationError as error:
            self.add_error('password', error)
        return value


class GetOTPRegisterCodeSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=4)

    def save(self, validated_data):
        refresh = RefreshToken.for_user(validated_data)
        return ({
            'user_id': validated_data.id,
            'success': True,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=False)
    new_password = serializers.CharField(required=False)

    def validate_new_password(self, value):
        # use django validation for password 
        try:
            password_validation.validate_password(value, self.instance)
        except serializers.ValidationError as error:
            self.add_error('password', error)
        return value


class ArtistSerializer(serializers.ModelSerializer):
    music_quantity = serializers.SerializerMethodField()
    recent_music = serializers.SerializerMethodField()
    popular_music = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Artist
        fields = ('id', 'name', 'image', 'music_quantity', 'recent_music', 'popular_music')

    def get_music_quantity(self, artist):
        return artist.musics.count()

    def get_recent_music(self, artist):
        request = self.context.get('request')
        # Get the 3 most recently added music tracks
        musics = artist.musics.order_by('-created_at')[:3]
        return MusicListSerializer(musics, many=True, context={'request': request}).data

    def get_popular_music(self, artist):
        request = self.context.get('request')
        # Get the 3 most popular music tracks
        musics = artist.musics.annotate(play_count=Count('favorite_musics')).filter(status=True).order_by('-play_count')[:3]
        return MusicListSerializer(musics, many=True, context={'request': request}).data
    
    def get_image(self, obj):
        request = self.context.get('request')
        # add base URL for cover music
        if obj.image:
            image_url = obj.image.url
            return request.build_absolute_uri(image_url)
        return None


class ArtistListSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = Artist
        fields = ('id', 'name', 'image')

    def get_image(self, obj):
        request = self.context.get('request')
        # add base URL for cover music
        if obj.image:
            image_url = obj.image.url
            return request.build_absolute_uri(image_url)
        return None

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
