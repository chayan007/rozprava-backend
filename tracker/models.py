from django.db import models

from base.models import BaseModel

from profiles.models import Profile


class Location(BaseModel):
    """Store all user location."""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    ip_address = models.GenericIPAddressField()
    country = models.JSONField()
    city = models.JSONField()
    coordinates = models.JSONField()

    def __str__(self):
        return f'{self.profile.user.username}: {self.ip_address}'
