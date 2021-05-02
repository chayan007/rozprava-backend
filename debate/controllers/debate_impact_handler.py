from django.db import IntegrityError
from django.db.models import Avg

from debate.models import Debate, DebateImpactHit

from profiles.models import Profile


class DebateImpactHandler:

    def __init__(self, debate_uuid: str):
        self.debate = Debate.objects.get(uuid=debate_uuid)

    def rate(self, profile: Profile, rating: int):
        try:
            impact_obj = DebateImpactHit.objects.create(
                profile=profile,
                impact=rating,
                debate=self.debate
            )
            return impact_obj
        except (IntegrityError, ValueError):
            return False

    def get_aggregate_impact(self):
        """Get aggregate debate impact hit for each debate."""
        debate_summary = DebateImpactHit.objects.filter(
            debate=self.debate
        ).annotate(
            average_impact=Avg('impact')
        ).values(
            'average_impact'
        )
        return round(getattr(debate_summary, 'average_impact', 0))
