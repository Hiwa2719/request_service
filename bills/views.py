from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import BillSerializer
from .permisssions import IsStaff

User = get_user_model()


@api_view()
@permission_classes([IsStaff])
def get_user_bills(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'this user does not exist'})

    bills = user.bill_set.all()
    serializer = BillSerializer(bills, many=True)
    return Response(serializer.data)
