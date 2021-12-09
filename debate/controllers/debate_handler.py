from django.shortcuts import get_object_or_404

from base.controllers.configuration_manager import ConfigurationManager
from base.utils.string import get_string_matching_coefficient

from case.models import Case

from debate.exceptions import RebuttalFailedException
from debate.models import Debate

from profiles.exceptions import UserValidationFailedException
from profiles.models import User

from tracker.controllers.location_handler import LocationHandler


class DebateHandler:

    def __init__(self, case_uuid: str = None):
        self.case = Case.objects.get(uuid=case_uuid) if case_uuid else None

    @staticmethod
    def get_based_on_case(case_slug: str) -> [Debate]:
        case = Case.records.get(slug=case_slug)
        debates = Debate.records.filter(
            case=case,
            pointer__isnull=True
        )
        return debates

    @staticmethod
    def get_rebuttals_for_debate(debate: Debate) -> [Debate]:
        return Debate.records.filter(
            pointer=debate
        ).order_by('created_at')

    def align_rebuttals_with_debates(self, debates: [Debate]) -> [Debate]:
        aligned_debates = []
        for debate in debates:
            aligned_debates.append(debate)
            rebuttals = self.get_rebuttals_for_debate(debate)
            if not rebuttals:
                continue
            aligned_debates.extend(rebuttals)
        return aligned_debates

    @staticmethod
    def get(debate_uuid: str) -> Debate:
        return Debate.records.get(uuid=debate_uuid)

    def create(self, user, ip_address, **kwargs) -> Debate:
        debate = Debate.objects.create(**{
            'profile': user.profile,
            'is_posted_anonymously': kwargs['is_posted_anonymously'],
            'case': self.case,
            'comment': kwargs['comment'],
            'inclination': kwargs.get('inclination'),
            'location': LocationHandler(user.profile.uuid).get_location(ip_address)
        })
        return debate

    @staticmethod
    def create_rebuttal(user, ip_address, **kwargs) -> Debate:
        original_debate = Debate.objects.get(uuid=kwargs['debate_uuid'])
        if original_debate and not original_debate.pointer:
            debate = Debate.objects.create(**{
                'profile': user.profile,
                'is_posted_anonymously': kwargs['is_posted_anonymously'],
                'case': original_debate.case,
                'comment': kwargs['comment'],
                'inclination': kwargs.get('inclination', not original_debate.inclination),
                'pointer': original_debate,
                'location': LocationHandler(user.profile.uuid).get_location(ip_address)
            })
            return debate
        raise RebuttalFailedException('Failed to upload rebuttal to the specific debate.')

    @staticmethod
    def change_debate_anonymity_status(user, debate_uuid):
        debate = Debate.records.get(uuid=debate_uuid)
        assert debate.profile == user.profile
        debate.is_posted_anonymously = not debate.is_posted_anonymously
        debate.save()

    @staticmethod
    def update(debate_uuid, **kwargs) -> Debate:
        debate = Debate.objects.get(uuid=debate_uuid)
        if kwargs.get('comment') and (get_string_matching_coefficient(debate.comment, kwargs.get('comment'))) > 0.8:
            debate.comment = kwargs.get('comment')
        debate.inclination = (
            kwargs.get('inclination', debate.inclination)
            if not kwargs.get('is_rebuttal', False)
            else debate.inclination
        )
        debate.save()
        return debate

    @staticmethod
    def delete(debate_uuid: str, user: User) -> None:
        debate = Debate.records.get(uuid=debate_uuid)
        if debate.profile != user.profile:
            raise UserValidationFailedException(f'{user.username} cannot delete debate.')
        debate.is_deleted = True
        debate.save()

        rebuttals = Debate.records.filter(pointer=debate)
        for rebuttal in rebuttals:
            rebuttal.is_deleted = True
            rebuttal.save()

    def vote_to_shift_to_opposite_indicator(self, debate_uuid: str):
        debate = Debate.records.get(uuid=debate_uuid)
        if debate.inclination:
            debate.votes_to_shift_to_against += 1
        else:
            debate.votes_to_shift_to_for += 1

        debate.save()

        shifting_threshold = ConfigurationManager().get('DEBATE_CONFIG')['SHIFTING_THRESHOLD']
        if debate.votes_to_shift_to_for > shifting_threshold or debate.votes_to_shift_to_against > shifting_threshold:
            self.shift_to_opposite_indicator(debate_uuid)

    @staticmethod
    def shift_to_opposite_indicator(debate_uuid: str):
        debate = Debate.records.get(uuid=debate_uuid)
        if debate.inclination:
            debate.inclination = Debate.InclinationChoices.AGAINST
        else:
            debate.inclination = Debate.InclinationChoices.FOR
        debate.save()
