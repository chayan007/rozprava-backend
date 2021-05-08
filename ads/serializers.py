from rest_framework.serializers import ModelSerializer

from ads.models import Boost

from case.serializers import CaseSerializer

from profiles.serializers import ProfileSerializer


class BoostSerializer(ModelSerializer):

    profile = ProfileSerializer()
    case = CaseSerializer()

    class Meta:
        model = Boost
        fields = (
            'profile',
            'case',
            'amount',
            'per_day_allotment',
            'start_date',
            'end_date'
        )
