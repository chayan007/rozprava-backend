from django.db import models

from base.models import BaseModel

from chat.utilities import get_one_to_one_chat_attachment_address

from profiles.models import Profile


class Message(BaseModel):
    """Store one to one messages."""

    sender = models.ForeignKey(Profile, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_seen = models.BooleanField(default=False)
    message = models.TextField(null=True, blank=True)
    attachment = models.FileField(upload_to=get_one_to_one_chat_attachment_address, null=True, blank=True)

    def __str__(self):
        return f'{self.sender.user.username} -> {self.receiver.user.username}'
