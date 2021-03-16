from rest_framework.generics import ListAPIView

from debate.models import Debate
from debate.serializers import DebateSerializer


class DebateListView(ListAPIView):
    """List all debates for a specific case."""

    serializer_class = DebateSerializer
    model = Debate
    paginate_by = 50

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug:
            queryset = self.model.records.filter(case__slug=slug)
        else:
            queryset = self.model.records.all()
        return queryset.order_by('-created_at')

