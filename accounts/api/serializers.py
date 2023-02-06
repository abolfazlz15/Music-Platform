from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


class LoginSerializer(serializers.Serializer):
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
            'success': True,
            'refresh': str(refresh),
            'access': str(refresh.access_token),

        })