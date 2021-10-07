from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from base.models import BaseModel

from profiles.models import Profile


class Activity(BaseModel):

    class ActivityChoices(models.IntegerChoices):
        REPORT = 0
        UPVOTE = 1
        DOWNVOTE = 2
        VIEW = 3

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    activity_type = models.IntegerField(choices=ActivityChoices.choices)

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=200)
    content_object = GenericForeignKey()

    class Meta:
        unique_together = ('content_type', 'object_id', 'profile', 'activity_type',)

    def __str__(self):
        return '{} -> {}'.format(
            self.profile.user.get_full_name(),
            self.get_activity_type_display()
        )


class HashTag(BaseModel):

    name = models.CharField(unique=True, max_length=100)
    views = models.BigIntegerField(default=0)

    def is_trending(self):
        if self.views > 100:
            return True
        return False

    def __str__(self):
        return self.name
