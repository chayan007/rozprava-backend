from rest_framework.serializers import ModelSerializer

from debate.models import Debate


class DebateSerializer(ModelSerializer):

    class Meta:
        model = Debate
        fields = ('profile', 'comment', 'inclination', 'impact')
