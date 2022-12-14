from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .permisssions import DeletePermission
from .serializers import BillSerializer

User = get_user_model()


@api_view()
@permission_classes([IsAdminUser])
def get_user_bills(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'this user does not exist'})

    bills = user.bill_set.all()
    serializer = BillSerializer(bills, many=True)
    return Response(serializer.data)


class BillViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated, DeletePermission]
    serializer_class = BillSerializer

    def get_queryset(self):
        user = self.request.user
        return user.bill_set.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

