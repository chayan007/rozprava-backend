from rest_framework import serializers

from case.models import Case

from profiles.serializers import ProfileSerializer


class CaseSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer()

    class Meta:
        model = Case
        fields = (
            'uuid',
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
