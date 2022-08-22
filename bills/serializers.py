from rest_framework import serializers
from .models import Bill
from services.serializers import ServiceSerializer, WageSerializer
from accounts.serializers import ProfileSerializer
from services.models import Wage
from rest_framework.validators import ValidationError


class CustomServiceField(serializers.RelatedField):
    def __init__(self, **kwargs):
        self.serializer = kwargs.pop('serializer')
        super().__init__(**kwargs)

    def get_queryset(self):
        if self.serializer:
            model = self.serializer.Meta.model
            return model.objects.all()
        return super().get_queryset()

    def to_internal_value(self, data):
        return self.get_queryset().get(id=data)

    def to_representation(self, value):
        return self.serializer(value).data


class CustomChoiceField(serializers.ChoiceField):
    def to_representation(self, obj):
        if obj == '' and self.allow_blank:
            return obj
        return self._choices[obj]


class BillSerializer(serializers.ModelSerializer):
    STATES = [
        ('CR', 'Created'),
        ('CK', 'Check'),
    ]

    service = CustomServiceField(serializer=ServiceSerializer)
    wage = WageSerializer(required=False)
    state = CustomChoiceField(choices=STATES)
    user = serializers.SerializerMethodField()

    class Meta:
        model = Bill
        fields = '__all__'

    def get_user(self, instance):
        profile = instance.user.profile
        serializer = ProfileSerializer(profile)
        return serializer.data

    def validate_state(self, state):
        if self.instance and self.instance.state in ['CK', 'DF']:
            raise ValidationError('Your are not allowed to update this bill anymore')
        return state

    def create(self, validated_data):
        validated_data = self.calculate_total_price_wage(validated_data)
        return super().create(validated_data)

    @staticmethod
    def calculate_total_price_wage(validated_data):
        service = validated_data['service']
        service_price = service.price
        user_type = validated_data['user'].profile.type
        wage = Wage.objects.get(user_type=user_type, service=service)
        total_price = service_price + service_price * wage.percentage / 100
        validated_data.update(total_price=total_price, wage=wage)
        return validated_data

    def update(self, instance, validated_data):
        service = validated_data.get('service')
        if service and service != instance.service:
            validated_data = self.calculate_total_price_wage(validated_data)
        return super().update(instance, validated_data)
