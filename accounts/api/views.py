from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api import serializers
from accounts.models import User
from accounts.otp_service import OTP


class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serializers.UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = serializer.save(validated_data=serializer.validated_data)
        return Response(result, status=status.HTTP_200_OK)


class UserRegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serializers.UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            clean_data = serializer.validated_data
            otp_service = OTP()
            otp_service.generate_otp(clean_data['email'])
            cache.set(key='register', value={'email': clean_data['email'], 'password': clean_data['password'], 'username': clean_data['username']}, timeout=300)

            return Response({'email': clean_data['email'], 'result': 'email sended'}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class GetOTPRegisterCodeView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = serializers.GetOTPRegisterCodeSerializer(data=request.data)
        user_data = cache.get(key='register')
        otp_service = OTP()
        if user_data is None:
            return Response({'error': 'this code not exist or invalid', 'success': False}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            clean_data = serializer.validated_data

            if otp_service.verify_otp(otp=clean_data['code'], email=user_data['email']):
                user = User.objects.create_user(email=user_data['email'], username=user_data['username'], password=user_data['password'])
                result = serializer.save(validated_data=user)
                return Response(result, status=status.HTTP_201_CREATED)

            return Response({'error': 'this code not exist or invalid', 'success': False}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class UserProfileView(APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        serializer = serializers.UserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)