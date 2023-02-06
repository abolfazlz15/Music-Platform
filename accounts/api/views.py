from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api import serializers


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save(validated_data=serializer.validated_data)
        return Response(result, status=status.HTTP_200_OK)