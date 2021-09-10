from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from base.utilities import get_client_ip

from debate.controllers.debate_handler import DebateHandler
from debate.controllers.debate_impact_handler import DebateImpactHandler
from debate.forms import DebateForm, RebuttalForm
from debate.models import Debate
from debate.serializers import DebateSerializer

from profiles.exceptions import UserValidationFailedException


class DebateListView(ListAPIView):
    """List all debates for a specific case."""

    serializer_class = DebateSerializer
    model = Debate
    paginate_by = 50

    def get_queryset(self):
        slug = self.request.query_params['slug']
        queryset = (
            DebateHandler().get_based_on_case(slug)
            if slug
            else self.model.records.all()
        )
        return queryset.order_by('-created_at')


class DebateView(GenericAPIView):
    """Handle all debate operations."""

    serializer_class = DebateSerializer

    def get(self, request, *args, **kwargs):
        """Get debate and it's respective rebuttals."""
        debate_handler = DebateHandler()
        debate = debate_handler.get(kwargs.get('debate_uuid'))
        rebuttals = debate_handler.get_rebuttals_for_debate(debate)
        return Response(
            status=status.HTTP_200_OK,
            data={
                'count': len(rebuttals),
                # TODO: Add pagination to this.
                'page': 0,
                'rebuttals': self.serializer_class(rebuttals, many=True).data
            }
        )

    def post(self, request, *args, **kwargs):
        """Post a debate against a case."""
        debate_form_validation = DebateForm(data=request.POST)
        if not debate_form_validation.is_valid():
            return Response(
                data=debate_form_validation.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        debate = DebateHandler(
            case_uuid=kwargs.get('case_uuid')
        ).create(
            user=request.user,
            ip_address=get_client_ip(request),
            **debate_form_validation.data
        )
        serialized_debate = self.serializer_class(debate)
        return Response(
            data=serialized_debate.data,
            status=status.HTTP_201_CREATED
        )

    def put(self, request, *args, **kwargs):
        """Update a debate against a case."""
        debate = DebateHandler().update(kwargs.get('debate_uuid'), **request.POST)
        serialized_debate = self.serializer_class(debate)
        return Response(
            data=serialized_debate.data,
            status=status.HTTP_202_ACCEPTED
        )


class RebuttalView(GenericAPIView):
    """Handle all rebuttal operations."""

    serializer_class = DebateSerializer

    def get(self, request, *args, **kwargs):
        """Get rebuttal and associated debate."""
        debate_handler = DebateHandler()
        rebuttal = debate_handler.get(kwargs.get('rebuttal_uuid'))
        debate = rebuttal.pointer
        return Response(
            status=status.HTTP_200_OK,
            data={
                'debate': self.serializer_class(debate).data,
                'rebuttal': self.serializer_class(rebuttal).data
            }
        )

    def post(self, request, *args, **kwargs):
        """Post rebuttal against a debate."""
        rebuttal_form_validation = RebuttalForm(data=request.POST)
        if not rebuttal_form_validation.is_valid():
            return Response(
                data=rebuttal_form_validation.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        rebuttal = DebateHandler(
            case_uuid=kwargs.get('case_uuid')
        ).create_rebuttal(
            user=request.user,
            ip_address=get_client_ip(request),
            **rebuttal_form_validation.data
        )
        serialized_rebuttal = self.serializer_class(rebuttal)
        return Response(
            data=serialized_rebuttal.data,
            status=status.HTTP_201_CREATED
        )

    def put(self, request, *args, **kwargs):
        """Update rebuttal against a debate."""
        rebuttal = DebateHandler().update(
            kwargs.get('rebuttal_uuid'),
            is_rebuttal=True,
            **request.POST
        )
        serialized_rebuttal = self.serializer_class(rebuttal)
        return Response(
            data=serialized_rebuttal.data,
            status=status.HTTP_202_ACCEPTED
        )


class DebateActivityView(GenericAPIView):
    """Record any activity on Debate as Like or Report."""

    serializer_class = DebateSerializer

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        if not profile:
            raise UserValidationFailedException('You need to be logged in to perform this action!')

        debate_uuid = kwargs.get('debate_uuid')
        activity_type = kwargs.get('activity_type')

        if debate_uuid and activity_type:
            debate = Debate.records.get(uuid=debate_uuid)
            debate.activities.create(activity_type=activity_type, profile=profile)
            return Response(
                data={'message': 'Wow! You have interacted with the debate.'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            data={'message': 'Oops! Something went wrong. Try again later.'},
            status=status.HTTP_304_NOT_MODIFIED
        )


class DebateImpactView(GenericAPIView):
    """Handle entire debate impact related flow."""

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        rating = request.data.get('rating')
        debate_uuid = kwargs['debate_uuid']

        impact_obj = DebateImpactHandler(debate_uuid).rate(profile, rating)
        if not impact_obj:
            return Response(
                data={'error': 'Failed to rate the debate!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            data={
                'message': 'Successfully rated the debate.',
                'impact': impact_obj.impact
            },
            status=status.HTTP_201_CREATED
        )

    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        debate_uuid = kwargs['debate_uuid']

        impact_obj = DebateImpactHandler(debate_uuid).get_impact_for_profile(profile)
        if not impact_obj:
            return Response(
                data={'error': 'User have not rated for this debate.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            data={'impact': impact_obj.impact},
            status=status.HTTP_200_OK
        )
