from django.contrib.auth.models import User
from django.db import models

from base.models import BaseModel


class Profile(BaseModel):
    """Profile class based on top of user."""

    class GenderChoices(models.TextChoices):

        MALE = 'MALE'
        FEMALE = 'FEMALE'
        TRANSGENDER = 'TRANS'
        OTHER = 'OTHER'

    class CelebrityRank(models.IntegerChoices):

        NOBODY = 0
        MICRO_INFLUENCER = 1
        INFLUENCER = 2
        CELEBRITY = 3
        SUPERSTAR = 4
        ADMIN = 5

    class RelationshipStatusChoices(models.IntegerChoices):

        SINGLE = 0
        ENGAGED = 1
        MARRIED = 2
        COMMITTED = 3
        WIDOWED = 4

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    display_pic = models.ImageField(upload_to='user/dp/', null=True, blank=True)
    mobile_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    country = models.CharField(max_length=30, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    celebrity_rank = models.SmallIntegerField(choices=CelebrityRank.choices, default=CelebrityRank.NOBODY.value)
    is_celebrity = models.BooleanField(default=False)
    profession = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    relationship_status = models.SmallIntegerField(choices=RelationshipStatusChoices.choices, default=RelationshipStatusChoices.SINGLE.value)

    def __str__(self):
        return self.user.get_full_name()


class Group(BaseModel):
    """Group of profiles."""

    class GroupPrivacy(models.IntegerChoices):
        """Privacy choices for a group."""
        PUBLIC = 0
        PRIVATE = 1

    name = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    profiles = models.ManyToManyField(Profile, related_name='members')
    profile_requests = models.ManyToManyField(Profile, related_name='pending_request_profiles')
    is_paid = models.BooleanField(default=False)
    admins = models.ManyToManyField(Profile, related_name='admins')
    privacy = models.SmallIntegerField(choices=GroupPrivacy.choices, default=GroupPrivacy.PUBLIC.value)
    interview = models.JSONField(null=True, blank=True)
    created_by = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='created_by')

    def __str__(self):
        return '{}: {} members'.format(self.name, self.profiles.count())


class FollowerMap(BaseModel):
    """Model to store followers."""

    follower = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='following')

    class Meta:

        unique_together = ('follower', 'following',)

    def __str__(self):
        return f'{self.follower} follows {self.following}'
