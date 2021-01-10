from django.shortcuts import get_object_or_404

from case.models import Case
from debate.models import Debate
from base.utils.string import get_string_matching_coefficient


class DebateHandler:

    def __init__(self, case_uuid):
        self.case = Case.objects.get(uuid=case_uuid)

    @staticmethod
    def get(debate_uuid):
        return get_object_or_404(Debate, uuid=debate_uuid)

    def create(self, user, **kwargs):
        debate = Debate.objects.create(**{
            'profile': user.profile,
            'case': self.case,
            'comment': kwargs['comment'],
            'inclination': kwargs.get('inclination'),
        })
        return debate

    @staticmethod
    def update(debate_uuid, **kwargs):
        debate = Debate.objects.get(uuid=debate_uuid)
        if kwargs.get('comment') and (get_string_matching_coefficient(debate.comment, kwargs.get('comment'))) > 0.8:
            debate.comment = kwargs.get('comment')
        debate.inclination = kwargs.get('inclination', debate.inclination)
        debate.save()
        return debate

    @staticmethod
    def delete(debate_uuid):
        debate = Debate.objects.get(uuid=debate_uuid)
        debate.delete()
