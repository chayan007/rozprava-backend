from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from ads.controllers.case_booster import CaseBooster
from ads.serializers import BoostSerializer


class CaseBoosterView(GenericAPIView):
    """Handles end to end case booster operations."""

    def get(self, request, *args, **kwargs):
        """Get list of all boosts for a profile."""
        boosts = CaseBooster(request.user.profile).list()
        paginated_boosts = self.paginate_queryset(boosts)
        serialized_boosts = BoostSerializer(paginated_boosts, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data=serialized_boosts.data
        )

    def post(self, request, *args, **kwargs):
        """Creates a post."""
        boost = CaseBooster(request.user.profile).create(
            case_uuid=request.data['case_uuid'],
            amount=request.data['amount'],
            start_date=request.data['start_date'],
            end_date=request.data['end_date']
        )
        serialized_boost = BoostSerializer(boost)
        return Response(
            status=status.HTTP_201_CREATED,
            data=serialized_boost.data
        )

    def put(self, request, boost_uuid: str):
        """Update an ad."""
        boost = CaseBooster(request.user.profile).update(
            boost_uuid=boost_uuid,
            additional_amount=request.data.get('additional_amount'),
            end_date=request.data.get('end_date')
        )
        serialized_boost = BoostSerializer(boost)
        return Response(
            status=status.HTTP_200_OK,
            data=serialized_boost.data
        )
