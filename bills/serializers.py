from rest_framework import serializers
from .models import Bill
from services.serializers import ServiceSerializer, WageSerializer
from accounts.serializers import ProfileSerializer


class BillSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()
    wage = WageSerializer()
    state = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = '__all__'

    def get_state(self, instance):
        return instance.get_state_display()

    def get_user(self, instance):
        profile = instance.user.profile
        serializer = ProfileSerializer(profile)
        return serializer.data
