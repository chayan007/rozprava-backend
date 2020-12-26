from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from activity.models import Activity, Tag

from base.models import BaseModel

from case.models import Case

from profiles.models import Profile

from proof.models import Proof


class Debate(BaseModel):

    class Inclination(models.IntegerChoices):

        FOR = 1
        AGAINST = 0

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    comment = models.TextField()

    proofs = models.ManyToManyField(Proof)
    activities = GenericRelation(Activity)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return '{} -> {}'.format(
            self.profile.user.get_full_name(),
            self.case.__str__()
        )
