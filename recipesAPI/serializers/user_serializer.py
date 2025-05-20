from django.contrib.auth.models import User
from rest_framework import serializers

from recipesAPI.models import UserProfile
from recipesAPI.validators import user_validators


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(
        max_length=20,
        required=True,
    )
    last_name = serializers.CharField(
        max_length=60,
        required=False,
    )

    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'first_name', 'last_name',
            'description', 'birth_date', 'favorite_recipe'
        ]

    def validate_first_name(self, value):
        return user_validators.min_length(value)

    def validate_last_name(self, value):
        return user_validators.min_length(value)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    email = serializers.EmailField(required=True)
    profile = UserProfileSerializer(required=True)

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
        profile_data = validated_data.pop('profile')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        return user


class UpdateUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)
    new_password = serializers.CharField(required=False, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'password', 'new_password', 'email', 'profile'
        ]

    def validate(self, attrs):
        user = self.context['request'].user
        password = attrs.get('password')

        if password:
            user_validators.current_password_check(user, attrs['password'])
        else:
            raise serializers.ValidationError(
                {'password': 'This field is required'}
            )
        return super().validate(attrs)

    def validate_username(self, value):
        return user_validators.validate_username(value)

    def validate_new_password(self, value):
        return user_validators.validate_password(value)

    def validate_email(self, value):
        return user_validators.validate_email(value)

    def update(self, instance, validated_data):
        user = self.context['request'].user

        profile_data = validated_data.pop('profile', None)
        new_password = validated_data.pop('new_password', None)
        validated_data.pop('password')

        if new_password:
            instance.set_password(new_password)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        if profile_data:
            if not user.profile:
                UserProfile.objects.create(user=user, **profile_data)
            else:
                for field, value in profile_data.items():
                    setattr(instance.profile, field, value)
            instance.profile.save()

        instance.save()

        return instance
