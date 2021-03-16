from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from case.models import Case
from case.serializers import CaseSerializer

from profiles.exceptions import UserValidationFailedException


class CaseListView(ListAPIView):
    """Get list of cases."""

    serializer_class = CaseSerializer
    model = Case
    paginate_by = 50

    def get_queryset(self):
        category = self.kwargs.get('category')
        if category:
            queryset = self.model.records.filter(uuid=category)
        else:
            queryset = self.model.records.all()
        return queryset.order_by('-created_at')


class CaseDetailView(RetrieveAPIView):
    """Retrieve specific case."""

    lookup_field = 'slug'
    queryset = Case.records.all()
    serializer_class = CaseSerializer


class CaseActivityView(APIView):
    """Record any activity on case as Like or Report."""

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        if not profile:
            raise UserValidationFailedException('You need to be logged in to perform this action!')

        case_uuid = kwargs.get('case_uuid')
        activity_type = kwargs.get('activity_type')

        if case_uuid and activity_type:
            case = Case.objects.get(uuid=case_uuid)
            case.activities.create(activity_type=activity_type, profile=profile)
            return Response(
                data={'message': 'Wow! You have interacted with the post.'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            data={'message': 'Oops! Something went wrong. Try again later.'},
            status=status.HTTP_304_NOT_MODIFIED
        )
