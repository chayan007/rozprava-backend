from rest_framework import serializers

from case.models import Case

from profiles.serializers import ProfileSerializer


class CaseSerializer(serializers.ModelSerializer):

    profile = serializers.SerializerMethodField()

    def get_profile(self, obj):
        if not obj.is_anonymous:
            return ProfileSerializer()

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
