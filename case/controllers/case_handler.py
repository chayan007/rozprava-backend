import datetime

from django.db.models import Count, Q
from django.utils.text import slugify

from base.constants import UNIQUE_DATETIME_FORMAT
from base.utils.string import get_string_matching_coefficient

from case.models import Case

from profiles.exceptions import UserValidationFailedException
from profiles.models import User

from tracker.controllers.location_handler import LocationHandler


class CaseHandler:

    @staticmethod
    def get(slug: str) -> Case:
        return Case.records.get(slug=slug)

    @staticmethod
    def search(search_value: str):
        queryset = Case.records.filter(Q(
            question__icontains=search_value
        ) | Q(
            description__icontains=search_value
        ))
        # TODO: Implement Group filtering by number of members.
        return queryset.annotate(joined_profiles=Count('profiles')).order_by('-joined_profiles')
        # return queryset

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
    def delete(slug: str, user: User) -> None:
        case = Case.records.get(slug=slug)
        if case.profile != user.profile:
            raise UserValidationFailedException(f'{user.username} cannot delete case.')
        case.is_deleted = True
        case.save()
