from django.contrib.auth.forms import AuthenticationForm
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login

from .serializers import ProfileSerializer, UserCreationSerializer


@api_view(['POST'])
def register_view(request):
    serializer = UserCreationSerializer(data=request.data)
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
