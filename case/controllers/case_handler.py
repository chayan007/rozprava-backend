from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from base.utils.string import get_string_matching_coefficient

from case.models import Case


class CaseHandler:

    @staticmethod
    def get(slug):
        return get_object_or_404(Case, slug=slug)

    @staticmethod
    def create(user, **kwargs):
        question = kwargs.get('question')
        case = Case.objects.create(**{
            'profile': user.profile,
            'question': question,
            'description': kwargs.get('description'),
            'category': int(kwargs.get('category')),
            'slug': slugify('{}-{}'.format(user.username, question)),
        })
        return case

    @staticmethod
    def update(slug, **kwargs):
        case = Case.objects.get(slug=slug)
        if kwargs.get('question') and (get_string_matching_coefficient(case.question, kwargs.get('question')) > 0.8):
            case.question = kwargs.get('question')

        case.description = kwargs.get('description', case.description)
        case.category = int(kwargs.get('category', case.category))
        case.save()
        return case

    @staticmethod
    def delete(slug):
        case = Case.objects.get(slug=slug)
        case.delete()
