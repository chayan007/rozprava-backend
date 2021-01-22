from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from activity.models import Activity, Tag

from base.models import BaseModel

from case.models import Case

from profiles.models import Profile

from proof.models import Proof

from tracker.models import Location


class Debate(BaseModel):

    class InclinationChoices(models.IntegerChoices):

        FOR = 1, _('For')
        AGAINST = 0, _('Against')

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    comment = models.TextField()
    inclination = models.SmallIntegerField(choices=InclinationChoices.choices, default=InclinationChoices.FOR.value)
    pointer = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    impact = models.SmallIntegerField(default=0, validators=[
        MaxValueValidator(5),
        MinValueValidator(0)
    ])

    proofs = models.ManyToManyField(Proof)
    activities = GenericRelation(Activity)
    tags = models.ManyToManyField(Tag)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '{} : {}'.format(
            self.profile.user.get_full_name(),
            self.case.__str__()
        )
