from rest_framework import serializers
from user.models import Extended


class ExtendedUserSerializer(serializers.Serializer):
    user = serializers.IntegerField(source='user.id', required=False)
    email = serializers.CharField(required=True, allow_blank=False, max_length=255)
    given_name = serializers.CharField(required=True, allow_blank=False, max_length=255)
    family_name = serializers.CharField(required=True, allow_blank=False, max_length=255)
    user_language = serializers.CharField(required=True, allow_blank=False, max_length=255)
    name = serializers.CharField(required=True, allow_blank=False, max_length=255)
    picture = serializers.CharField(required=True, allow_blank=False, max_length=255)

    class Meta:
        model = Extended

    def create(self, validated_data):
        extended = Extended.objects.create(**validated_data)
        return extended