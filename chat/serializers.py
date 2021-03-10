from rest_framework import serializers

from chat.models import OneToOneMessage

from profiles.serializers import ProfileSerializer


class OneToOneMessageSerializer(serializers.ModelSerializer):

    sender = ProfileSerializer()
    receiver = ProfileSerializer()

    class Meta:
        model = OneToOneMessage
        fields = (
            'sender',
            'receiver',
            'is_seen',
            'message',
            'media',
        )
