from rest_framework import serializers


class StrictPayloadSerializer(serializers.ModelSerializer):
    def to_internal_value(self, data):
        unexpected = set(data) - set(self.fields)

        if unexpected:
            raise serializers.ValidationError({
                field: 'Non-Existent Field' for field in unexpected
            })

        return super().to_internal_value(data)
