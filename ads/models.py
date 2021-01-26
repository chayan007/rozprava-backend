from django.db import models

from ads.utilities import get_ads_image_upload_path, get_ads_video_upload_path

from base.models import BaseModel

from profiles.models import Profile


class Ad(BaseModel):
    """Store different Ads published on our website."""

    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to=get_ads_image_upload_path, null=True, blank=True)
    video = models.FileField(upload_to=get_ads_video_upload_path, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    starting_date = models.DateField()
    ending_date = models.DateField()
    payment_id = models.CharField(max_length=200, null=True, blank=True)
    is_event = models.BooleanField(default=False)

    def __str__(self):
        return self.name
