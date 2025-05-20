from django.contrib.auth.models import User
from rest_framework import serializers

from utils.password import strong_password_check


def min_length(value):
    if len(value) < 3:
        raise serializers.ValidationError(
            'This field must have be at least 3 characters'
        )
    return value


def validate_username(value):
    if len(value) < 3:
        raise serializers.ValidationError(
            'Username must be have at least 3 characters'
        )
    elif User.objects.filter(username=value):
        raise serializers.ValidationError('Username already registered')
    return value


def validate_password(value):
    errors = []

    if len(value) < 8:
        errors.append('Password must have be at least 8 characters')

    if not strong_password_check(value):
        errors.append(
            'Password must be have one lower, upper, digit and punctuation.')

    if errors:
        raise serializers.ValidationError(errors)
    return value


def current_password_check(user, value):
    if not user.check_password(value):
        raise serializers.ValidationError(
            {'password': 'Password is incorrect'})
    return value


def validate_email(value):
    if User.objects.filter(email=value).exists():
        raise serializers.ValidationError('Email already registered')
    return value
