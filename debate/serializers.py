from rest_framework import serializers

from debate.models import Debate
from debate.utilities import get_debate_impact, get_debate_metrics

from profiles.serializers import ProfileSerializer

from proof.serializers import ProofSerializer


class DebateSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer()
    proofs = ProofSerializer(many=True)
    activities = serializers.SerializerMethodField()
    impact = serializers.SerializerMethodField

    def get_activities(self, obj):
        return get_debate_metrics(obj)

    def get_impact(self, obj):
        return get_debate_impact(obj)

    class Meta:
        model = Debate
        fields = (
            'profile',
            'comment',
            'inclination',
            'proofs',
            'activities',
            'impact'
        )
