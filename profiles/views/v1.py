from django.db.models import Q, Count
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response

from profiles.controllers.group_handler import GroupObjectHandler, GroupProfileHandler
from profiles.controllers.profile_interest_handler import ProfileInterestHandler
from profiles.exceptions import UserValidationFailedException
from profiles.models import Profile
from profiles.serializers import ProfileSerializer, GroupSerializer


class ProfileView(GenericAPIView):
    """Individual profile view."""

    def get(self, request, username: str):
        """Get profile by username."""
        user_name = username or request.user.username
        profile = Profile.objects.get(user__username=user_name)
        serialized_profile = ProfileSerializer(profile)
        return Response(
            status=status.HTTP_200_OK,
            data=serialized_profile.data
        )


class ProfileListView(ListAPIView):
    """Get list of profiles."""

    serializer_class = ProfileSerializer()
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


class ProfileUpdateView(GenericAPIView):
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


class PasswordUpdateView(GenericAPIView):

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


class GroupView(GenericAPIView):

    def post(self, request, *args, **kwargs):
        """Create a group."""
        name = request.data['name']
        description = request.data['description']
        is_paid = request.data.get('is_paid', 0)

        group = GroupObjectHandler().create(
            profile=request.user.profile,
            name=name,
            description=description,
            is_paid=is_paid,
        )

        if not group:
            return Response(
                data={'error': 'Could not create group'},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            data={
                'message': 'Group has been created',
                'name': group.name,
                'is_paid': group.is_paid
            },
            status=status.HTTP_201_CREATED
        )

    def get(self, request, *args, **kwargs):
        """Get list of groups or just a group."""
        group_uuid = kwargs.get('group_uuid')
        group_handler = GroupObjectHandler()

        # If group_id is present, then directly serve the Group details.
        groups = [group_handler.get(group_uuid)] if group_uuid else group_handler.list()

        if not groups:
            return Response(
                data={'error': 'No group found'},
                status=status.HTTP_404_NOT_FOUND
            )

        paginated_groups = self.paginate_queryset(groups)
        serialized_groups = GroupSerializer(paginated_groups, many=True)

        return Response(
            data={'groups': serialized_groups.data},
            status=status.HTTP_200_OK
        )

    def delete(self, request, group_uuid: str):
        """Retire a group."""
        is_retired = GroupObjectHandler().retire(
            request.user.profile,
            group_uuid
        )
        if is_retired:
            return Response(
                data={'message': 'Group has been retired.'},
                status=status.HTTP_200_OK
            )
        return Response(
            data={'error': 'Group has not been retired.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class JoinGroupView(GenericAPIView):

    def post(self, request, group_uuid: str):
        """Join a group."""
        group_profile_handler = GroupProfileHandler(group_uuid)
        has_joined = group_profile_handler.join(request.user.profile)

        if has_joined:
            return Response(
                data={'message': 'Successfully joined the group.'},
                status=status.HTTP_200_OK
            )

        return Response(
            data={'error': 'Failed to join the group.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class LeaveGroupView(GenericAPIView):

    def post(self, request, group_uuid: str):
        """Leave a group."""
        group_profile_handler = GroupProfileHandler(group_uuid)
        has_left = group_profile_handler.leave(request.user.profile)

        if has_left:
            return Response(
                data={'message': 'Successfully left the group.'},
                status=status.HTTP_200_OK
            )

        return Response(
            data={'error': 'Failed to leave the group.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class GroupAdminChangeView(GenericAPIView):

    def post(self, request, group_uuid: str):
        """Add admin to a group."""
        group_profile_handler = GroupProfileHandler(group_uuid)
        added_admin = group_profile_handler.make_admin(
            request.user.profile,
            request.query_params['profile_uuid']
        )

        if added_admin:
            return Response(
                data={'message': 'Successfully added the admin.'},
                status=status.HTTP_200_OK
            )

        return Response(
            data={'error': 'Failed to add as admin.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class ProfileInterestView(GenericAPIView):
    """Handle e2e flow of ProfileInterest."""

    def post(self, request, *args, **kwargs):
        """Add interests to profile."""
        ProfileInterestHandler(
            request.user.profile
        ).add(
            request.data.get('categories')
        )
        return Response(
            data={'message': 'Added category(s) to profile interest.'},
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        """Remove interests from profile."""
        ProfileInterestHandler(
            request.user.profile
        ).remove(
            request.data.get('categories')
        )
        return Response(
            data={'message': 'Removed category(s) from profile interest.'},
            status=status.HTTP_200_OK
        )
