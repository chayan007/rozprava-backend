from django.db import IntegrityError

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

    def get_impact(self):
        return DebateImpactHit.objects.get(debate=self.debate)
