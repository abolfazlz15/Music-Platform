from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.cache import cache
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import generic
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, permissions, status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.api import serializers
from accounts.forms import ForotPasswordForm
from accounts.models import Artist, ImageProfile, User
from accounts.services.otp import OTP


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

    def get(self, request, pk):
        user = get_object_or_404(User, id=pk)
        serializer = serializers.UserSerializer(instance=user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ImageProfileListView(generics.ListAPIView):
    serializer_class = serializers.ImageListSerializer
    queryset = ImageProfile.objects.all()


class UserUpdateProfileView(APIView):

    def put(self, request):
        user = request.user
        serializer = serializers.UserProfileUpdateSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'data': serializer.data, 'success': True}, status=status.HTTP_200_OK)
        return Response({'errors': serializer.errors, 'success': False}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(UpdateAPIView):
        """
        An endpoint for changing password.
        """
        serializer_class = serializers.ChangePasswordSerializer
        model = User

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
        serializer = serializers.ArtistDetailSerializer(instance=instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

   
class ForgotPasswordView(APIView):
    serializer_class = serializers.ForgotPasswordSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'email': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            reset_url = reverse(
                "accounts:change_password",
                kwargs={"encoded_pk": encoded_pk, "token": token},
            )
            reset_link = f'{request.get_host()}/{reset_url}'
            message = render_to_string('accounts/forgot_password_link.html', {
                'link': reset_link,
            })
            to_email = email
            email = EmailMessage(
                'بازیابی ایمیل',
                message,
                to=[to_email]
            )
            email.send()
            return Response({'detail': 'Password reset link sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(generic.View): # template base
    form_class = ForotPasswordForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'accounts/forgot_password.html', context={'form': form})
    
    def post(self, request, *args, **kwargs):
        try:
            token = kwargs.get('token')
            encoded_pk = kwargs.get('encoded_pk')

            pk = urlsafe_base64_decode(encoded_pk).decode()
            user = User.objects.get(pk=pk)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist) as e:
            return None

        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            if PasswordResetTokenGenerator().check_token(user, token):
                password = data['new_password']
                confirm_password = data['new_password_confirm']
                if password != confirm_password:
                    messages.add_message(request, messages.WARNING, 'رمز عبور شما مطابقت ندارد')
                user.set_password(password)
                user.save()
                return redirect('accounts:reset_password_done')  
            else:
                messages.add_message(request, messages.WARNING, 'مشکلی وجود دارد، لطفا دوباره امتحان کنید')
        return render(request, 'accounts/forgot_password.html', context={'form': form})


class RestPasswordDoneView(generic.TemplateView):
    template_name = 'accounts/reset_password_done.html'