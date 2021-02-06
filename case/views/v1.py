from rest_framework.generics import ListAPIView

from case.models import Case
from case.serializers import CaseSerializer


class CaseListView(ListAPIView):
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
