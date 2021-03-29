from rest_framework import serializers

from notification.models import Notification

from profiles.serializers import ProfileSerializer


class NotificationSerializer(serializers.ModelSerializer):
    """Serializer for the notification model."""

    profile = ProfileSerializer()

    class Meta:
        model = Notification
        fields = (
            'profile',
            'message',
            'type',
            'is_read'
        )
