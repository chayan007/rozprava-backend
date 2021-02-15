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

    FIELDS_ALLOWED_TO_BE_UPDATED = [
        'dob', 'mobile_number', 'address', 'country',
        'profession', 'gender', 'relationship_status'
    ]

    def post(self, request, *args, **kwargs):
        profile = request.user.profile
        for field in self.FIELDS_ALLOWED_TO_BE_UPDATED:
            setattr(
                profile,
                field,
                request.data.get(field) or getattr(profile, field)
            )
        try:
            profile.save()
            return Response(
                data={'message': 'Profile has been updated.'},
                status=status.HTTP_201_CREATED
            )
        except (AttributeError, ValueError, KeyError):
            return Response(
                data={'error': 'Profile could not be updated.'},
                status=status.HTTP_201_CREATED
            )


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
                status=status.HTTP_201_CREATED
            )
        raise UserValidationFailedException('New passwords supplied does not match!')
