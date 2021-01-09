from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import BaseModel


class Profile(BaseModel):
    """Profile class based on top of user."""

    class GenderChoices(models.TextChoices):

        MALE = 'MALE', _('Male')
        FEMALE = 'FEMALE', _('Female')
        TRANSGENDER = 'TRANS', _('Transgender')

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
    celebrity_rank = models.SmallIntegerField(choices=CelebrityRank, default=CelebrityRank.NOBODY.value)
    profession = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=10, choices=GenderChoices.choices)
    relationship_status = models.SmallIntegerField(choices=RelationshipStatusChoices, default=RelationshipStatusChoices.SINGLE.value)

    def __str__(self):
        return self.user.get_full_name()


class Group(BaseModel):
    """Group of profiles."""

    name = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    profiles = models.ManyToManyField(Profile)

    def __str__(self):
        return '{}: {} members'.format(self.name, self.profiles.count())
