from django.contrib.auth.models import User
from rest_framework import serializers

from recipesAPI.validators import user_validators


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    email = serializers.EmailField(required=True)

    def validate_username(self, value):
        return user_validators.validate_username(value)

    def validate_password(self, value):
        return user_validators.validate_password(value)

    def validate_email(self, value):
        return user_validators.validate_email(value)

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class GetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email',]


class SecurityUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'new_password']

    new_password = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['password'] = user_validators.current_password_check(
            user,
            attrs['password']
        )
        return super().validate(attrs)

    def validate_username(self, value):
        return user_validators.validate_username(value)

    def validate_new_password(self, value):
        return user_validators.validate_password(value)

    def update(self, instance, validated_data):
        new_password = validated_data.get('new_password')

        if new_password:
            validated_data.pop('password', None)
            instance.set_password(new_password)
        else:
            validated_data.pop('password', None)
            validated_data.pop('new_password', None)

        return super().update(instance, validated_data)


class ProfileUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        user = self.context['request'].user
        attrs['password'] = user_validators.current_password_check(
            user,
            attrs['password']
        )
        return super().validate(attrs)

    def validate_email(self, value):
        return user_validators.validate_email(value)

    def update(self, instance, validated_data):
        validated_data.pop('password', None)
        return super().update(instance, validated_data)
