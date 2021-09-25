from rest_framework import serializers

from case.models import Case
from case.utilities import get_case_metrics

from profiles.serializers import ProfileSerializer

from proof.serializers import ProofSerializer


class CaseSerializer(serializers.ModelSerializer):

    profile = serializers.SerializerMethodField()
    metrics = serializers.SerializerMethodField()
    proofs = ProofSerializer(many=True)

    def get_profile(self, obj):
        if not obj.is_anonymous:
            return ProfileSerializer(obj.profile).data

    def get_metrics(self, obj):
        return get_case_metrics(obj)

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
            'against_label',
            'metrics',
            'created_at',
            'proofs'
        )


class CaseDetailedSerializer:
    pass
