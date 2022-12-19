from rest_framework import serializers
from team.models import Team, Member


class TeamSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False, max_length=100)
    settings = serializers.JSONField()

    class Meta:
        model = Team

    def create(self, validated_data):
        model = Team.objects.create(**validated_data)
        return model

