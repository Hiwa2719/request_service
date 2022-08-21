from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import ProfileSerializer, UserCreationSerializer


@api_view(['POST'])
def register_view(request):
    serializer = UserCreationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        serializer = ProfileSerializer(user.profile)
        return Response(serializer.data)
    return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
