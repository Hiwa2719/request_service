from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError
from rest_framework import serializers

from .models import Profile, USER_TYPES

User = get_user_model()


class UserCreationSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    type = serializers.ChoiceField(choices=USER_TYPES, default='t')

    def validate_email(self, email):
        queryset = User.objects.filter(username=email)
        if self.instance:
            queryset = queryset.exclude(username=self.instance.username)
        if queryset.exists():
            raise serializers.ValidationError('this email already exists')
        return email

    def validate(self, attrs):
        user = User(username=attrs['email'])
        try:
            password_validation.validate_password(attrs['password'], user)
        except ValidationError as error:
            raise serializers.ValidationError(error.messages)
        return attrs

    def create(self, validated_data):
        profile_type = validated_data.pop('type')
        user = User.objects.create_user(username=validated_data['email'], **validated_data)
        Profile.objects.create(type=profile_type, user=user)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'email', 'first_name', 'last_name',


class ProfileSerializer(serializers.Serializer):
    user = UserSerializer()
    type = serializers.SerializerMethodField()

    def get_type(self, instance):
        return instance.get_type_display()