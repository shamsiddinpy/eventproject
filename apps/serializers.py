# events/serializers.py
from rest_framework import serializers

from apps.models import Event
from users.serializers import UserSerializer


class EventSerializer(serializers.ModelSerializer):
    created_by_username = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location',
                  'created_by', 'created_by_username', 'created_at', 'updated_at']
        read_only_fields = ['created_by', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)


class EventDetailSerializer(EventSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta(EventSerializer.Meta):
        pass
