from rest_framework.generics import ListAPIView, RetrieveAPIView

from case.models import Case
from case.serializers import CaseSerializer


class CaseListView(ListAPIView):
    """Get list of cases."""

    serializer_class = CaseSerializer
    model = Case
    paginate_by = 50

    def get_queryset(self):
        category = self.kwargs.get('category')
        if category:
            queryset = self.model.objects.filter(uuid=category)
        else:
            queryset = self.model.objects.all()
        return queryset.order_by('-created_at')


class CaseDetailView(RetrieveAPIView):
    """Retrieve specific case."""

    lookup_field = 'slug'
    queryset = Case.objects.all()
    serializer_class = CaseSerializer
