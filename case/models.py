from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from activity.models import Activity, Tag

from base.models import BaseModel

from profiles.models import Profile

from proof.models import Proof


class Case(BaseModel):

    class CaseCategory(models.IntegerChoices):

        OTHER = 0
        POLITICS = 1
        SPORTS = 2
        EDUCATION = 3
        ADULT = 4
        SPIRITUAL = 5
        ENTERTAINMENT = 6
        BUSINESS = 7
        TECHNOLOGY = 8
        NATURE = 9

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.CharField(max_length=450)
    description = models.TextField()
    category = models.SmallIntegerField(choices=CaseCategory, default=CaseCategory.OTHER.value)
    slug = models.CharField(max_length=200)

    proofs = models.ManyToManyField(Proof)
    activities = GenericRelation(Activity)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return '[{}] -> {}'.format(
            self.get_category_display(),
            self.profile.user.get_full_name()
        )
