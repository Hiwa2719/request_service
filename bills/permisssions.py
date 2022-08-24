from rest_framework.permissions import BasePermission

from .models import BillStates


class DeletePermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE':
            if obj.state in [BillStates.CHECK, BillStates.FINALIZED]:
                self.message = 'Sorry your are not allowed to delete this request anymore.'
                return False
        return True
