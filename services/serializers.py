from rest_framework import serializers
from .models import Wage, Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'


class WageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wage
        fields = '__all__'
