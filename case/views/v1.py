from rest_framework.generics import ListAPIView

from case.models import Case
from case.serializers import CaseSerializer


class CaseListView(ListAPIView):
    serializer_class = CaseSerializer
    model = Case
    paginate_by = 50

    def get_queryset(self):
        poster_id = self.kwargs['poster_id']
        queryset = self.model.objects.filter(poster_id=poster_id)
        return queryset.order_by('-post_time')
