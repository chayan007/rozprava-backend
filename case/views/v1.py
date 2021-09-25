from django.db.models import Count
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from base.utilities import get_client_ip

from case.controllers.case_handler import CaseHandler
from case.forms import CaseForm
from case.models import Case
from case.serializers import CaseSerializer

from profiles.exceptions import UserValidationFailedException


class CaseListView(ListAPIView):
    """Get list of cases."""

    serializer_class = CaseSerializer
    model = Case
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        category = self.kwargs.get('category')
        username = self.kwargs.get('username')
        is_ordered = bool(self.kwargs.get('is_ordered', 0))
        return CaseHandler().filter(category, username, is_ordered)


class CaseSearchView(GenericAPIView):

    def get(self, request, search_value):
        """Search cases based on the search_value passed."""
        case_handler = CaseHandler()
        cases = case_handler.search(search_value)
        if not cases:
            return Response(
                data={'error': 'No cases found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serialized_cases = CaseSerializer(cases, many=True)
        return Response(
            data={'cases': serialized_cases.data},
            status=status.HTTP_200_OK
        )


class CaseView(GenericAPIView):
    """Handles cases CRUD operations."""

    serializer_class = CaseSerializer

    def get(self, request, slug):
        """Get one single case based on slug."""
        case = CaseHandler().get(slug)
        if not case:
            return Response(
                data={'error': 'No case found! Please try again with proper details.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serialized_case = self.serializer_class(case)
        return Response(
            data=serialized_case.data,
            status=status.HTTP_200_OK
        )

    def put(self, request, slug):
        """Edit an existing case."""
        case = CaseHandler().update(slug, **request.POST)
        serialized_case = self.serializer_class(case)
        return Response(
            data=serialized_case.data,
            status=status.HTTP_202_ACCEPTED
        )

    def post(self, request, *args, **kwargs):
        """Create a case."""
        case_form_validation = CaseForm(data=request.data)
        if not case_form_validation.is_valid():
            return Response(
                data=case_form_validation.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        case = CaseHandler().create(
            user=request.user,
            ip_address=get_client_ip(request),
            **case_form_validation.data
        )
        serialized_case = self.serializer_class(case)
        return Response(
            data=serialized_case.data,
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, slug):
        """Delete specific case."""
        try:
            CaseHandler().delete(slug, request.user)
            return Response(
                data={'message': 'Case has been successfully deleted.'},
                status=status.HTTP_200_OK
            )
        except UserValidationFailedException:
            return Response(
                data={'message': f'{request.user.username} cannot delete this case.'},
                status=status.HTTP_403_FORBIDDEN
            )
        except Exception as err:
            return Response(
                data={'message': str(err)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CaseActivityView(APIView):
    """Record any activity on case as Like or Report."""

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        if not profile:
            raise UserValidationFailedException('You need to be logged in to perform this action!')

        case_uuid = kwargs.get('case_uuid')
        activity_type = kwargs.get('activity_type')

        if case_uuid and activity_type:
            case = Case.records.get(uuid=case_uuid)
            case.activities.create(activity_type=activity_type, profile=profile)
            return Response(
                data={'message': 'Wow! You have interacted with the post.'},
                status=status.HTTP_201_CREATED
            )
        return Response(
            data={'message': 'Oops! Something went wrong. Try again later.'},
            status=status.HTTP_304_NOT_MODIFIED
        )


class RecommendCaseView(ListAPIView):
    """Get list of recommended cases."""

    model = Case
    paginate_by = 9
    serializer_class = CaseSerializer

    def get_queryset(self):
        # TODO: Implement better logic for cases recommendations after beta is released.
        queryset = self.model.objects.all()
        queryset.annotate(activity_hype=Count('acitvity')).order_by('-activity_hype')
        return queryset.order_by('-created_at')
