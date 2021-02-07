from rest_framework import serializers

from case.models import Case


class CaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Case
        fields = (
            'profile',
            'question',
            'description',
            'category',
            'slug',
            'for_label',
            'against_label'
        )


class CaseDetailedSerializer:
    pass
