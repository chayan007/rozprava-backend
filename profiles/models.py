from django.contrib.auth.models import User
from django.db import models

from base.models import BaseModel

from profiles.utilities import get_profile_verification_image_upload_path


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


class IdentityDocument(BaseModel):

    class IdentityChoices(models.TextChoices):

        UIDAI = 'UIDAI'
        PAN = 'PAN'
        PASSPORT = 'PASSPORT'
        DRIVING_LICENSE = 'DRIVING_LICENSE'
        VOTER_ID = 'VOTER_ID'
        OTHER = 'OTHER'

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    identity_type = models.CharField(max_length=20, choices=IdentityChoices.choices, default=IdentityChoices.OTHER.value)
    image = models.ImageField(upload_to=get_profile_verification_image_upload_path)
    id_number = models.CharField(max_length=100, null=True, blank=True)
    kyc_json = models.JSONField(null=True, blank=True)
    is_valid = models.BooleanField(default=False)
    is_audited = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.profile.user.get_full_name()}'


class Group(BaseModel):
    """Group of profiles."""

    name = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    profiles = models.ManyToManyField(Profile)
    is_paid = models.BooleanField(default=False)

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
