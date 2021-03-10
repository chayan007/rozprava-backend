from typing import Any

from django.db.models import Count, Case, When, Q

from chat.models import OneToOneMessage

from profiles.models import Profile


class ChatEngine:

    def __init__(self, receiver_profile_uuid, sender_profile_uuid=None):
        self.sender = Profile.objects.get(uuid=sender_profile_uuid) if sender_profile_uuid else None
        self.receiver = Profile.objects.get(uuid=receiver_profile_uuid) if sender_profile_uuid else None

    def send(self, message: str = None, media: Any = None):
        """Send message handler."""
        try:
            OneToOneMessage.objects.create(
                sender=self.sender,
                receiver=self.receiver,
                message=message,
                media=media
            )
            return True
        except BaseException:
            return False

    def receive(self, **kwargs):
        """Receive message handler."""
        try:
            messages = OneToOneMessage.objects.filter(
                sender=self.sender,
                receiver=self.receiver
            )
            self.update_message_as_seen(messages)
            return messages
        except BaseException:
            return False

    def show_messaging_list(self):
        """Show messages unread/read grouped by user."""
        distinct_profile_uuids = OneToOneMessage.records.values_list(
            'sender__uuid', flat=True
        ).filter(
            receiver=self.receiver
        ).distinct('sender').order_by('created_at')

        message_list = Profile.objects.filter(
            uuid__in=distinct_profile_uuids
        ).annotate(
            no_of_unreads=Count(
                'one_to_one_message',
                filter=Q(one_to_one_message__is_seen=False)
            )
        )
        return message_list

    @staticmethod
    def update_message_as_seen(messages: [OneToOneMessage]):
        for message in messages:
            if not message.is_seen:
                message.is_seen = True
                message.save()

    def list_messages(self):
        try:
            return OneToOneMessage.objects.filter(receiver=self.receiver)
        except BaseException:
            return
