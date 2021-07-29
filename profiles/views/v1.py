from django.db.models import Q, Count
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from sentry_sdk import capture_exception

from base.constants import COMMON_ERROR_MESSAGE

from profiles.controllers.authentication import Authenticator
from profiles.controllers.group_handler import GroupObjectHandler, GroupProfileHandler
from profiles.controllers.profile_handler import ProfileHandler
from profiles.controllers.profile_interest_handler import ProfileInterestHandler
from profiles.exceptions import UserValidationFailedException
from profiles.models import Profile
from profiles.serializers import ProfileSerializer, GroupSerializer


class ProfileView(GenericAPIView):
    """Individual profile view."""

    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request, user_string: str):
        """Get profile by username."""
        if '@' in user_string:
            profile = Profile.objects.get(user__email=user_string)
        else:
            profile = Profile.objects.get(user__username=user_string)
        serialized_profile = self.serializer_class(profile, context={'request': request})
        return Response(
            status=status.HTTP_200_OK,
            data=serialized_profile.data
        )

    def put(self, request, username: str):
        """Update profile details."""
        profile = ProfileHandler(
            request.user.profile.uuid
        ).update_details(request.data)
        if profile:
            if profile.user.username != username:
                raise UserValidationFailedException(COMMON_ERROR_MESSAGE)

            serialized_profile = self.serializer_class(profile, context={'request': request})
            message = {
                'message': f'Profile {request.user.username} details has been updated.',
                'profile': serialized_profile.data
            }
        else:
            message = {'error': 'Failed to update profile details.'}
        return Response(
            data=message,
            status=status.HTTP_202_ACCEPTED
        )


class ProfileListView(ListAPIView):
    """Get list of profiles."""

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

    def put(self, request, *args, **kwargs):
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
            capture_exception()
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

    serializer_class = GroupSerializer

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
        group_handler = GroupObjectHandler()

        groups = group_handler.list()

        if not groups:
            return Response(
                data={'error': 'No group found'},
                status=status.HTTP_404_NOT_FOUND
            )

        paginated_groups = self.paginate_queryset(groups)
        serialized_groups = self.serializer_class(paginated_groups, many=True)

        return Response(
            data={'groups': serialized_groups.data},
            status=status.HTTP_200_OK
        )


class GroupSearchView(GenericAPIView):

    def get(self, request, group_uuid: str):
        """Get list of groups or just a group."""
        group_handler = GroupObjectHandler()

        group = group_handler.get(group_uuid)

        if not group:
            return Response(
                data={'error': 'No group found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serialized_groups = GroupSerializer(group)

        return Response(
            data={'groups': serialized_groups.data},
            status=status.HTTP_200_OK
        )


class GroupDeleteView(GenericAPIView):

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
            data={
                'error': ('Failed to join the group. In case there are already '
                          '6 members, you need to opt for paid group.')
            },
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

    serializer_class = GroupSerializer

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


class ResetPasswordCheckUserView(GenericAPIView):

    def get(self, request, user_string: str):
        """Get profile by username/email."""
        try:
            profile = (Profile.objects.get(user__email=user_string) if '@' in user_string else Profile.objects.get(user__username=user_string))
            data = {'username': profile.user.username}
        except Profile.DoesNotExist:
            data = {'error': 'No records found for the username / email.'}

        return Response(
            status=status.HTTP_200_OK,
            data=data
        )


class ResetPasswordSendOTPView(GenericAPIView):

    authenticator_class = Authenticator()

    def post(self, request, username: str):
        """Send OTP to user."""
        profile = Profile.objects.get(user__username=username)
        self.authenticator_class.initiate_reset_password(profile.user.email)

        return Response(
            status=status.HTTP_200_OK,
            data={'message': 'OTP has been sent.'}
        )


class ResetPasswordVerifyOTPView(GenericAPIView):

    authenticator_class = Authenticator()

    def put(self, request, username: str, otp: int):
        """Verify OTP sent to user."""
        is_verified = self.authenticator_class.verify_otp(username, otp)

        return Response(
            status=status.HTTP_200_OK if is_verified else status.HTTP_400_BAD_REQUEST,
            data={'status': bool(is_verified)}
        )


class ResetPasswordView(GenericAPIView):

    authenticator_class = Authenticator()

    def put(self, request, username: str):
        """Reset password given by user."""
        is_done = self.authenticator_class.reset_password(
            username,
            request.data.get('password')
        )

        return Response(
            status=status.HTTP_202_ACCEPTED if is_done else status.HTTP_400_BAD_REQUEST,
            data={'status': bool(is_done)}
        )
