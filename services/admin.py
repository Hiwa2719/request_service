from django.contrib import admin

from .models import Service, Wage


@admin.register(Service)
class ServiceModelAdmin(admin.ModelAdmin):
    list_display = '__str__', 'price'
    list_editable = 'price',
    search_fields = '__str__',
    ordering = 'name',


@admin.register(Wage)
class WageModelAdmin(admin.ModelAdmin):
    list_display = '__str__', 'percentage'
    list_editable = 'percentage',
    search_fields = '__str__',
    ordering = 'service__name',
