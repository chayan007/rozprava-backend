from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from base.utils.string import get_string_matching_coefficient

from case.models import Case

from tracker.controllers.location_handler import LocationHandler


class CaseHandler:

    @staticmethod
    def get(slug) -> Case:
        return get_object_or_404(Case, slug=slug)

    @staticmethod
    def filter_by_category(category: int) -> [Case]:
        return Case.objects.filter(
            category=category
        )

    @staticmethod
    def create(user: User, ip_address: str, **kwargs) -> Case:
        question = kwargs.get('question')
        case = Case.objects.create(**{
            'profile': user.profile,
            'question': question,
            'description': kwargs.get('description'),
            'category': int(kwargs.get('category')),
            'slug': slugify('{}-{}'.format(user.username, question)),
            'location': LocationHandler().get_location(ip_address),
            'for_label': kwargs.get('for_label'),
            'against_label': kwargs.get('against_label')
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
        case.delete()
