from django.contrib.auth.models import User
from PIL import Image
from rest_framework import serializers

from recipesAPI.models import UserProfile
from recipesAPI.serializers.common_serializer import StrictPayloadSerializer
from recipesAPI.validators import user_validators


class UserProfileSerializer(StrictPayloadSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'first_name', 'last_name',
            'description', 'birth_date', 'favorite_recipe'
        ]

    def validate_first_name(self, value):
        return user_validators.min_length(value)


class UserSerializer(StrictPayloadSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True)
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'email', 'profile',
        ]

    def validate_username(self, value):
        return user_validators.validate_username(value)

    def validate_password(self, value):
        return user_validators.validate_password(value)

    def validate_email(self, value):
        return user_validators.validate_email(value)

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        user = User.objects.create_user(**validated_data)
        if profile_data:
            UserProfile.objects.create(user=user, **profile_data)
        return user


class UpdateUserSerializer(StrictPayloadSerializer):
    avatar = serializers.ImageField(
        source='profile.avatar',
        required=False,
        write_only=True
    )
    profile = UserProfileSerializer(required=False)
    new_password = serializers.CharField(required=False, write_only=True)
    password = serializers.CharField(required=False, write_only=True)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = [
            'username', 'password', 'new_password', 'email', 'profile', 'avatar'
        ]

    def validate(self, attrs):
        user = self.context['request'].user
        password = attrs.get('password')
        new_password = attrs.get('new_password')
        email = attrs.get('email')

        if (new_password or email) and not password:
            raise serializers.ValidationError(
                {'password': 'This field is required'}
            )
        if new_password or email:
            user_validators.current_password_check(user, attrs['password'])

        return super().validate(attrs)

    def validate_username(self, value):
        return user_validators.validate_username(value)

    def validate_new_password(self, value):
        return user_validators.validate_password(value)

    def validate_email(self, value):
        return user_validators.validate_email(value)

    def validate_avatar(self, value):
        max_size = 1 * 1024 * 1024

        if value.size > max_size:
            raise serializers.ValidationError(
                f"The image max size is {max_size / (1024 * 1024)} MB.")

        try:
            with Image.open(value) as img:
                img.verify()

        except Exception:
            raise serializers.ValidationError("This is not valid image")

        value.seek(0)

        return value

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', None)
        new_password = validated_data.pop('new_password', None)
        validated_data.pop('password', None)

        if new_password:
            instance.set_password(new_password)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        profile, _ = UserProfile.objects.get_or_create(user=instance)
        if profile_data:
            for field, value in profile_data.items():
                setattr(profile, field, value)
            profile.save()

        return instance
