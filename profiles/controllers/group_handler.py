from typing import Union

from django.db import IntegrityError
from django.db.models import Q, Count
from sentry_sdk import capture_exception

from base.controllers.configuration_manager import ConfigurationManager

from profiles.exceptions import InvalidPermissionException
from profiles.models import Group, Profile


class GroupObjectHandler:

    @staticmethod
    def create(
        profile: Profile,
        name: str,
        is_paid: bool,
        description: Union[str, None],
        members: list = None
    ) -> Union[Group, bool]:
        """Create a group and add the user as admin."""
        try:
            group = Group.objects.create(
                name=name,
                description=description,
                is_paid=is_paid,
                created_by=profile
            )

            # Add group creator as Admin
            group.profiles.add(profile)
            group.admins.add(profile)

            # Add other members
            for username in members:
                try:
                    member_profile = Profile.objects.get(user__username=username)
                    group.profiles.add(member_profile)
                except Exception:
                    continue

            group.save()
            return group
        except (AttributeError, IntegrityError):
            capture_exception()
            return False

    @staticmethod
    def retire(profile: Profile, group_uuid: str) -> bool:
        """Retire a group."""
        try:
            group = Group.objects.get(uuid=group_uuid)

            if profile not in group.admins:
                raise AssertionError('This user does not have rights to retire a group.')

            group.is_deleted = True
            group.save()
            return True
        except (AssertionError, AttributeError, IntegrityError, ValueError):
            capture_exception()
            return False

    @staticmethod
    def get(group_uuid: str) -> Group:
        return Group.objects.get(uuid=group_uuid)

    @staticmethod
    def search(group_name: str):
        queryset = Group.records.filter(Q(
            name__icontains=group_name
        ) | Q(
            description__icontains=group_name
        ))
        # TODO: Implement Group filtering by number of members.
        return queryset.annotate(joined_profiles=Count('profiles')).order_by('-joined_profiles')
        # return queryset

    @staticmethod
    def list() -> [Group]:
        return Group.objects.all()


class GroupProfileHandler:

    def __init__(self, group_uuid: str):
        self.group = Group.objects.get(uuid=group_uuid)

    def join(self, profile: Profile) -> bool:
        """Add profile to a group."""
        try:
            if (
                not self.group.is_paid and
                len(self.group.profiles) > ConfigurationManager().get('FREE_TIER_MAX_MEMBERS')
            ):
                raise InvalidPermissionException('You need to purchase paid plan to add more members.')

            self.group.profiles.add(profile)
            self.group.save()
            return True
        except (AttributeError, IntegrityError, ValueError):
            capture_exception()
            return False

    def leave(self, username: str, auth_profile: Profile) -> bool:
        """Remove profile from a group."""
        try:
            profile = Profile.objects.get(user__username=username)
            if profile != auth_profile and auth_profile not in self.group.admins:
                return False
            self.group.profiles.remove(profile)
            if profile in self.group.admins:
                self.group.admins.remove(profile)
            self.group.save()
            return True
        except (AttributeError, IntegrityError, ValueError):
            capture_exception()
            return False

    def make_admin(self, admin_profile: Profile, profile_uuid: str) -> bool:
        """Make profile a group admin."""
        if admin_profile not in self.group.admins:
            raise InvalidPermissionException('Only admins are allowed to create admins.')

        try:
            profile = Profile.objects.get(uuid=profile_uuid)

            self.group.profiles.remove(profile)
            self.group.save()
            return True
        except (AttributeError, IntegrityError, ValueError):
            capture_exception()
            return False
