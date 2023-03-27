from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api import serializers
from accounts.models import Artist, User
from accounts.otp_service import OTP
from drf_yasg.utils import swagger_auto_schema



class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = serializers.UserLoginSerializer
    @swagger_auto_schema(request_body=serializers.UserLoginSerializer)
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

            return Response({'email': clean_data['email'], 'result': 'email sended', 'success': True}, status=status.HTTP_202_ACCEPTED)
        return Response({'errors': serializer.errors, 'success': False}, status=status.HTTP_406_NOT_ACCEPTABLE)


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
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        serializer = serializers.UserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserUpdateProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = serializers.UserProfileUpdateSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = serializers.ChangePasswordSerializer
        model = User
        permission_classes = [permissions.IsAuthenticated]

        def get_object(self, queryset=None):
            obj = self.request.user
            return obj

        def update(self, request, *args, **kwargs):
            self.object = self.get_object()
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                # Check old password
                if not self.object.check_password(serializer.data.get("old_password")):
                    return Response({"old_password": ["Wrong password."], 'status': False}, status=status.HTTP_400_BAD_REQUEST)
                # set_password also hashes the password that the user will get
                self.object.set_password(serializer.data.get("new_password"))
                self.object.save()
                response = {
                    'status': True,
                    'code': status.HTTP_200_OK,
                    'message': 'Password updated successfully',
                }

                return Response(response)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ArtistProfileView(generics.GenericAPIView):
    def get(self, request, pk):
        instance = Artist.objects.get(id=pk)
        serializer = serializers.ArtistSerializer(instance=instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArtistListView(generics.ListAPIView):
    serializer_class = serializers.ArtistListSerializer
    queryset = Artist.objects.all()

    
