from rest_framework import serializers
from .models import Bill


class BillSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = '__all__'

    def get_state(self, instance):
        return instance.get_state_display()
