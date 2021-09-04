import datetime

from django.contrib.auth.models import User
from django.db.models import Count
from django.utils.text import slugify

from base.constants import UNIQUE_DATETIME_FORMAT
from base.utils.string import get_string_matching_coefficient

from case.models import Case

from tracker.controllers.location_handler import LocationHandler


class CaseHandler:

    @staticmethod
    def get(slug: str) -> Case:
        return Case.records.get(slug=slug)

    @staticmethod
    def filter(category: int = None, username: str = None, is_ordered: bool = False) -> [Case]:
        cases = Case.records.all()
        if category:
            cases = cases.filter(category=category)
        if username:
            cases = cases.filter(profile__user__username=username)
        # return (
        #     cases.annotate(activity_hype=Count('activities')).order_by('-activity_hype')
        #     if not is_ordered
        #     else cases.order_by('created_at')
        # )
        return cases.order_by('created_at')

    @staticmethod
    def create(user: User, ip_address: str, **kwargs) -> Case:
        question = kwargs.get('question')
        case = Case.objects.create(**{
            'profile': user.profile,
            'question': question,
            'description': kwargs.get('description'),
            'category': int(kwargs.get('category')),
            'slug': slugify(f"{user.username}-{datetime.datetime.now().strftime(UNIQUE_DATETIME_FORMAT)}-{question[:20]}"),
            # 'location': LocationHandler().get_location(ip_address),
            'for_label': kwargs.get('for_label'),
            'against_label': kwargs.get('against_label'),
            'is_anonymous': bool(kwargs.get('is_anonymous', 0))
        })
        return case

    @staticmethod
    def update(slug: str, **kwargs) -> Case:
        case = Case.objects.get(slug=slug)

        case.question = kwargs.get('question') if (
                kwargs.get('question') and
                (get_string_matching_coefficient(case.question, kwargs.get('question')) > 0.8)
        ) else case.question

        case.description = kwargs.get('description', case.description) if (
                kwargs.get('description') and
                (get_string_matching_coefficient(case.description, kwargs.get('description')) > 0.8)
        ) else case.description

        case.for_label = kwargs.get('for_label', case.for_label) if (
                kwargs.get('for_label') and
                (get_string_matching_coefficient(case.for_label, kwargs.get('for_label')) > 0.8)
        ) else case.for_label

        case.against_label = kwargs.get('against_label', case.against_label) if (
                kwargs.get('against_label') and
                (get_string_matching_coefficient(case.against_label, kwargs.get('against_label')) > 0.8)
        ) else case.against_label

        case.category = int(kwargs.get('category', case.category))

        case.save()
        return case

    @staticmethod
    def delete(slug: str) -> None:
        case = Case.objects.get(slug=slug)
        case.is_deleted = True
        case.save()
