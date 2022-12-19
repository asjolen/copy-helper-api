from rest_framework import serializers
from object.models import Access


class AccessSerializer(serializers.Serializer):
    object = serializers.IntegerField(source='object.id')
    user_access = serializers.IntegerField(source='user.id', required=False)
    team_access = serializers.IntegerField(source='team.id', required=False)

    class Meta:
        model = Access

    def create(self, validated_data):
        model = Access.objects.create(**validated_data)
        return model