from django.contrib import admin
from .models import Bill


@admin.register(Bill)
class BillModelAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user = request.user
        if user.has_perm('bills.only_check_bills') and not user.is_superuser:
            return queryset.filter(state='CK')
        return queryset

    def get_readonly_fields(self, request, obj=None):
        if request.user.has_perm('bills.only_check_bills'):
            return ['service', 'user', 'user_extra_description', 'wage', 'photo', 'total_price']
        return self.readonly_fields
