from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from base.models import BaseModel
from profiles.models import Profile


class Activity(BaseModel):

    class ActivityChoices(models.IntegerChoices):
        REPORT = 0
        LIKE = 1

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    activity_type = models.SmallIntegerField(choices=ActivityChoices)

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

    class Meta:
        unique_together = ('content_object', 'profile', 'activity_type',)

    def __str__(self):
        return '{} -> {}'.format(
            self.profile.user.get_full_name(),
            self.get_activity_type_display()
        )


class Tag(BaseModel):

    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        return self.name
