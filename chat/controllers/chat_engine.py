from chat.models import OneToOneMessage

from profiles.models import Profile


class ChatEngine:

    def __init__(self, sender_profile_uuid, receiver_profile_uuid):
        self.sender = Profile.objects.get(uuid=sender_profile_uuid)
        self.receiver = Profile.objects.get(uuid=receiver_profile_uuid)

    def send(self, **kwargs):
        """Send message handler."""
        try:
            OneToOneMessage.objects.create(
                sender=self.sender,
                receiver=self.receiver,
                message=kwargs.get('message', None),
                media=kwargs.get('media', None)
            )
            return True
        except BaseException:
            return False

    def receive(self, **kwargs):
        """Send message handler."""
        try:
            return OneToOneMessage.objects.filter(
                sender=self.sender,
                receiver=self.receiver
            )
        except BaseException:
            return False
