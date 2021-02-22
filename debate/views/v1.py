from rest_framework.generics import ListAPIView

from activity.models import Activity

from case.models import Case

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
            queryset = self.model.objects.filter(case__slug=slug)
        else:
            queryset = self.model.objects.all()
        return queryset.order_by('-created_at')

