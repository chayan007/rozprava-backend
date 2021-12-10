from debate.models import Debate

from profiles.models import Profile


class ProfileMeter:

    def __init__(self, profile_uuid: str):
        self.profile = Profile.objects.get(uuid=profile_uuid)

    @staticmethod
    def get_score():
        return 0


class RageProfileMeter(ProfileMeter):

    def __init__(self, profile_uuid: str):
        super().__init__(profile_uuid)

    def get_score(self):
        debates = Debate.records.filter(profile=self.profile)
        for_count = debates.filter(inclination=Debate.InclinationChoices.FOR.value).count()
        against_count = debates.filter(inclination=Debate.InclinationChoices.AGAINST.value).count()

        resistance_score = (for_count * 0.25 + against_count * 0.75) / (for_count + against_count)
        support_score = (for_count * 0.75 + against_count * 0.25) / (for_count + against_count)

        return {
            'rage': (resistance_score + support_score) / 2,
            'resistance': resistance_score,
            'support': support_score
        }

