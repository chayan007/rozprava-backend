from django.db import models

from base.models import BaseModel

from profiles.models import Profile


class Notification(BaseModel):
    """Model to store all notifications."""

    class NotificationType(models.IntegerChoices):

        OTHER = 0
        SMS = 1
        EMAIL = 2
        PUSH = 3
        CALL = 4

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    message = models.TextField()
    type = models.SmallIntegerField(choices=NotificationType.choices, default=NotificationType.EMAIL.value)
    is_read = models.BooleanField(default=False)
    redirect_url = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f'{self.get_type_display()}: {self.profile.user.get_full_name()}'
