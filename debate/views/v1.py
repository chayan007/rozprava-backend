from rest_framework.generics import GenericAPIView, ListAPIView

from debate.controllers.debate_handler import DebateHandler
from debate.models import Debate
from debate.serializers import DebateSerializer


class DebateListView(ListAPIView):
    """List all debates for a specific case."""

    serializer_class = DebateSerializer
    model = Debate
    paginate_by = 50

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        queryset = (
            DebateHandler().get_based_on_case(slug)
            if slug
            else self.model.records.all()
        )
        return queryset.order_by('-created_at')


class DebateView(GenericAPIView):
    """Handle all debate operations."""

    def get(self, request, *args, **kwargs):
        """Get debate and it's rebuttals."""
        pass

    def post(self, request, *args, **kwargs):
        """Post a debate against a case."""
        pass

    def put(self, request, *args, **kwargs):
        """Update a debate against a case."""
        pass


class RebuttalView(GenericAPIView):
    """Handle all rebuttal operations."""

    def get(self, request, *args, **kwargs):
        """Get rebuttal and associated debate."""
        pass

    def post(self, request, *args, **kwargs):
        """Post rebuttal against a debate."""
        pass

    def put(self, request, *args, **kwargs):
        """Update rebuttal against a debate."""
        pass
