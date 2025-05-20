from rest_framework import serializers


def title_validator(value):
    if len(value) < 3:
        raise serializers.ValidationError('Title is too short')
    return value


def has_value(value):
    if not value:
        raise serializers.ValidationError('This field is required')
    return value
