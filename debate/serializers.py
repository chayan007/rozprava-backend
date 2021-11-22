from rest_framework import serializers

from debate.controllers.debate_impact_handler import DebateImpactHandler
from debate.models import Debate
from debate.utilities import get_debate_metrics

from profiles.serializers import ProfileSerializer

from proof.serializers import ProofSerializer


class DebateSerializer(serializers.ModelSerializer):

    profile = serializers.SerializerMethodField()
    proofs = ProofSerializer(many=True)
    activities = serializers.SerializerMethodField()
    impact = serializers.SerializerMethodField()

    def get_activities(self, obj):
        return get_debate_metrics(obj)

    def get_profile(self, obj):
        if not obj.is_posted_anonymously:
            return ProfileSerializer(obj.profile).data

    def get_impact(self, obj):
        return DebateImpactHandler(obj.uuid).get_aggregate_impact()

    class Meta:
        model = Debate
        fields = (
            'uuid',
            'profile',
            'comment',
            'inclination',
            'proofs',
            'activities',
            'impact'
        )
