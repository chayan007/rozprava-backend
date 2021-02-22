from rest_framework.serializers import ModelSerializer

from proof.models import Proof

from profiles.serializers import ProfileSerializer


class DebateSerializer(ModelSerializer):

    profile = ProfileSerializer

    class Meta:
        model = Proof
        fields = ('profile', 'file')
