from rest_framework import serializers
from organization.models import Organization, Member


class OrganizationSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False, max_length=255)
    website = serializers.CharField(required=False, allow_blank=True, max_length=255)

    class Meta:
        model = Organization

    def create(self, validated_data):
        model = Organization.objects.create(**validated_data)
        return model

