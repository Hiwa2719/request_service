from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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
        user = User.objects.create_user(username=validated_data['email'], is_active=False, **validated_data)
        Profile.objects.create(type=profile_type, user=user)
        self.send_email(user)
        return user

    def send_email(self, user):
        message = render_to_string('accounts/email_template.html', {
            'user': user,
            'domain': get_current_site(request=self._context['request']).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        send_mail(subject='Email Verification', message='Your Email verification Link',
                  from_email='hiahmadyan@gmail.com', recipient_list=[user.email], html_message=message)

    def update(self, instance, validated_data):
        password = validated_data.pop('password')
        profile_type = validated_data.pop('type')
        queryset = User.objects.filter(username=instance.username)
        queryset.update(**validated_data)
        user = queryset.first()
        if password:
            user.set_password(password)
            user.save()
        if profile_type:
            profile = user.profile
            profile.type = profile_type
            profile.save()
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


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        # todo update for valid token
        self.username_field = 'username'
        attrs['username'] = attrs['email']
        data = super().validate(attrs)
        del data['refresh']
        serializer = UserSerializer(self.user)
        data.update(serializer.data)
        return data
