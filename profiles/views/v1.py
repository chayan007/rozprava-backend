from django.db.models import Q, Count
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.exceptions import UserValidationFailedException
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
        if request.data.get('check_old_password'):
            if not request.user.check_password(
                request.data.get('old_password').strip()
            ):
                raise UserValidationFailedException('Old password provided is wrong!')
        if request.data.get('new_password1').strip() == request.data.get('new_password2').strip():
            request.user.set_password(request.data.get('new_password1').strip())
            request.user.save()
            return Response(
                data={'message': 'Password has been changed.'},
                status=status.HTTP_200_OK
            )
        raise UserValidationFailedException('New passwords supplied does not match!')
