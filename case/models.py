from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from activity.models import Activity, HashTag

from base.models import BaseModel

from profiles.models import Profile, Group

from proof.models import Proof

from tracker.models import Location


class Case(BaseModel):

    class CaseCategory(models.IntegerChoices):

        OTHER = 0, _('Other')
        POLITICS = 1, _('Politics')
        SPORTS = 2, _('Sports')
        EDUCATION = 3, _('Education')
        ADULT = 4, _('Adult')
        SPIRITUAL = 5, _('Spiritual')
        ENTERTAINMENT = 6, _('Entertainment')
        BUSINESS = 7, _('Business')
        TECHNOLOGY = 8, _('Technology')
        NATURE = 9, _('Nature')

    class CaseStatus(models.IntegerChoices):

        REVOKED = 0, _('Revoked')
        ACTIVE = 1, _('Active')
        UNDER_REVIEW = 2, _('Under Review')

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.CharField(max_length=450)
    description = models.TextField(null=True, blank=True)
    category = models.SmallIntegerField(choices=CaseCategory.choices, default=CaseCategory.OTHER.value)
    slug = models.CharField(max_length=200)
    for_label = models.CharField(max_length=100, default='For')
    against_label = models.CharField(max_length=100, default='Against')
    status = models.SmallIntegerField(choices=CaseStatus.choices, default=CaseStatus.ACTIVE.value)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    proofs = models.ManyToManyField(Proof)
    activities = GenericRelation(Activity)
    tags = models.ManyToManyField(HashTag)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '[{}] -> {}'.format(
            self.get_category_display(),
            self.profile.user.get_full_name()
        )


class ProfileInterest(BaseModel):
    """Record profile interests."""

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    category = models.IntegerField(null=False, blank=False, validators=[
        MaxValueValidator(len(Case.CaseCategory.choices) + 1),
        MinValueValidator(0)
    ])

    def __str__(self):
        return self.profile.user.get_full_name()

    class Meta:

        unique_together = ('profile', 'category',)
