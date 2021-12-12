from rest_framework import serializers

from activity.models import Activity

from case.models import Case
from case.utilities import get_case_metrics

from profiles.serializers import ProfileSerializer
from profiles.utilities import check_if_request_authenticated

from proof.serializers import ProofSerializer


class CaseSerializer(serializers.ModelSerializer):

    profile = serializers.SerializerMethodField()
    metrics = serializers.SerializerMethodField()
    proofs = ProofSerializer(many=True)
    activity = serializers.SerializerMethodField()

    def get_activity(self, obj):
        request = self.context.get('request')
        if not check_if_request_authenticated(request):
            return {}

        return Activity.objects.values_list(
            'activity_type',
            flat=True
        ).filter(
            content_type__model='case',
            object_id=obj.uuid,
            profile=request.user.profile
        )

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
            'proofs',
            'activity'
        )


class CaseDetailedSerializer:
    pass
