from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from activity.models import Activity, HashTag

from base.models import BaseModel

from case.models import Case

from profiles.models import Profile

from proof.models import Proof

from tracker.models import Location


class Debate(BaseModel):
    """Model to store debate."""

    class InclinationChoices(models.IntegerChoices):

        FOR = 1, _('For')
        AGAINST = 0, _('Against')

    class DebateStatus(models.IntegerChoices):

        REVOKED = 0, _('Revoked')
        ACTIVE = 1, _('Active')
        UNDER_REVIEW = 2, _('Under Review')

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    is_posted_anonymously = models.BooleanField(default=False)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    comment = models.TextField()
    inclination = models.SmallIntegerField(choices=InclinationChoices.choices, default=InclinationChoices.FOR.value)
    pointer = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    status = models.SmallIntegerField(choices=DebateStatus.choices, default=DebateStatus.ACTIVE.value)

    votes_to_shift_to_for = models.IntegerField(default=0)
    votes_to_shift_to_against = models.IntegerField(default=0)

    proofs = models.ManyToManyField(Proof, null=True, blank=True)
    activities = GenericRelation(Activity, null=True, blank=True)
    tags = models.ManyToManyField(HashTag, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return '{} : {}'.format(
            self.profile.user.get_full_name(),
            self.case.__str__()
        )


class DebateImpactHit(BaseModel):
    """Model to store debate impact mappings."""

    debate = models.ForeignKey(Debate, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    impact = models.SmallIntegerField(default=0, validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])

    def __str__(self):
        return f'{self.impact}: {self.profile.user.username}'

    class Meta:
        unique_together = ('profile', 'debate',)
