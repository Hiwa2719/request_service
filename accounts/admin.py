from django.contrib import admin
from .models import Profile
from django.contrib import messages
from django.utils.translation import ngettext


@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = '__str__', 'type'
    list_editable = 'type',
    search_fields = '__str__', 'type'

    actions = ['make_golden', 'make_silver', 'make_typical']

    @admin.action(description='make selected as Golden')
    def make_golden(self, request, queryset):
        updated = queryset.update(type='g')
        self.send_message(request, updated)

    @admin.action(description='make selected as Silver')
    def make_silver(self, request, queryset):
        updated = queryset.update(type='s')
        self.send_message(request, updated)

    @admin.action(description='make selected as Typical')
    def make_typical(self, request, queryset):
        updated = queryset.update(type='t')
        self.send_message(request, updated)

    def send_message(self, request, updated):
        self.message_user(request, ngettext(
            '%d story was successfully marked as published.',
            '%d stories were successfully marked as published.',
            updated,
        ) % updated, messages.SUCCESS)
