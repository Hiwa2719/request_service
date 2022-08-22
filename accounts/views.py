from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from .serializers import ProfileSerializer, UserCreationSerializer, MyTokenObtainPairSerializer
from django.contrib.auth.forms import PasswordResetForm
User = get_user_model()


@api_view(['POST'])
def register_view(request):
    serializer = UserCreationSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.save()
        serializer = ProfileSerializer(user.profile)
        return Response(serializer.data)
    return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        data = {
            'username': request.data.get('email'),
            'password': request.data.get('password')
        }
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)


def get_user_from_uidb64(uidb64):
    try:
        pk = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=pk)
    except (User.DoesNotExist, TypeError, ValueError, OverflowError):
        user = None
    return user


@api_view()
def activate_email(request, uidb64, token):
    user = get_user_from_uidb64(uidb64)

    if user and not user.is_active and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({'success': 'your email has been verified'})
    return Response({'error': 'Email verification failed'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    old_password = request.data.get('old_password')
    user = request.user
    if user.check_password(old_password):
        user = request.user
        data = {
            'email': user.email,
            'password': request.data.get('new_password')
        }
        serializer = UserCreationSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            serializer = ProfileSerializer(user.profile)
            return Response(serializer.data)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Sorry Old password is wrong'}, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def password_reset(request):
    email = request.query_params.get('email')
    form = PasswordResetForm({'email': email})
    if form.is_valid():
        opts = {
            "use_https": request.is_secure(),
            "token_generator": default_token_generator,
            "from_email": None,
            "email_template_name": "registration/password_reset_email.html",
            "subject_template_name": "registration/password_reset_subject.txt",
            "request": request,
            "html_email_template_name": None,
            "extra_email_context": None,
        }
        form.save(**opts)
        return Response({'success': 'a token has been sent to your email, please check your inbox'})
    return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def password_reset_confirm(request, uidb64, token):
    user = get_user_from_uidb64(uidb64)

    if user and user.is_active and default_token_generator.check_token(user, token):
        data = {
            'email': user.email,
            'password': request.data.get('password')
        }
        serializer = UserCreationSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': 'your password is now update'})
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    return Response({'error': 'Sorry provided link has issue'})
