from django.db import models

from base.models import BaseModel

from profiles.models import Profile


class Location(BaseModel):
    """Store all user location."""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    ip_address = models.GenericIPAddressField()
    country = models.CharField(max_length=150, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    coordinates = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return f'{self.profile.user.username}: {self.ip_address}'
