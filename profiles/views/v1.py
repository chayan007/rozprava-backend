from django.db.models import Q, Count
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView

from profiles.models import Profile
from profiles.serializers import ProfileSerializer


class ProfileListView(ListAPIView):
    """Get list of profiles."""

    serializer_class = ProfileSerializer
    model = Profile
    paginate_by = 50

    def get_queryset(self):
        search_username = self.request.query_params.get('username', None)
        if search_username:
            queryset = self.model.objects.filter(Q(
                user__username__icontains=search_username
            ) | Q(
                user__first_name__icontains=search_username
            ) | Q(
                user__last_name__icontains=search_username
            ))
        else:
            queryset = self.model.objects.all()
        queryset.annotate(follower_count=Count('follower')).order_by('-follower_count')
        return queryset.order_by('-created_at')


class ProfileUpdateView(APIView):
    """Update profile details."""

    def post(self, request, *args, **kwargs):
        pass


class PasswordUpdateView(APIView):

    def post(self, request, *args, **kwargs):
        pass
