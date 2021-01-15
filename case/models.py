from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.utils.translation import gettext_lazy as _

from activity.models import Activity, Tag

from base.models import BaseModel

from profiles.models import Profile

from proof.models import Proof


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

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.CharField(max_length=450)
    description = models.TextField(null=True, blank=True)
    category = models.SmallIntegerField(choices=CaseCategory.choices, default=CaseCategory.OTHER.value)
    slug = models.CharField(max_length=200)
    for_key = models.CharField(max_length=100, default='For')
    against_key = models.CharField(max_length=100, default='Against')

    proofs = models.ManyToManyField(Proof)
    activities = GenericRelation(Activity)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return '[{}] -> {}'.format(
            self.get_category_display(),
            self.profile.user.get_full_name()
        )
