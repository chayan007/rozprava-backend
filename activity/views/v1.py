from rest_framework.generics import ListAPIView

from activity.models import Activity
from activity.serializers import ActivitySerializer


class ActivityListView(ListAPIView):
    """List all activity for a specific profile."""

    serializer_class = ActivitySerializer
    model = Activity
    paginate_by = 10

    def get_queryset(self):
        queryset = Activity.records.filter(profile=self.request.user.profile)
        return queryset.order_by('-created_at')

