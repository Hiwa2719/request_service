from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import ProfileSerializer, UserCreationSerializer

User = get_user_model()


@api_view(['POST'])
def register_view(request):
    serializer = UserCreationSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.save()
        serializer = ProfileSerializer(user.profile)
        return Response(serializer.data)
    return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    data = {
        'username': request.data.get('email'),
        'password': request.data.get('password')
    }

    form = AuthenticationForm(data=data)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        serializer = ProfileSerializer(user.profile)
        return Response(serializer.data)
    return Response({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def activate_email(request, uidb64, token):
    try:
        pk = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=pk)
    except (User.DoesNotExist, TypeError, ValueError, OverflowError):
        user = None

    if user and not user.is_active and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({'success': 'your email has been verified'})
    return Response({'error': 'Email verification failed'}, status=status.HTTP_400_BAD_REQUEST)
