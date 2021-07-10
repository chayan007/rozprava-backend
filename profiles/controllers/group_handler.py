from typing import Union

from django.db import IntegrityError
from sentry_sdk import capture_exception

from base.controllers.configuration_manager import ConfigurationManager

from profiles.exceptions import UserValidationFailedException
from profiles.models import Group, Profile


class GroupObjectHandler:

    @staticmethod
    def create(
        profile: Profile,
        name: str,
        is_paid: bool,
        description: Union[str, None]
    ) -> Union[Group, bool]:
        """Create a group and add the user as admin."""
        try:
            group = Group.objects.create(
                name=name,
                description=description,
                is_paid=is_paid,
                created_by=profile
            )

            group.profiles.add(profile)
            group.admins.add(profile)
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
                return False

            self.group.profiles.add(profile)
            self.group.save()
            return True
        except (AttributeError, IntegrityError, ValueError):
            capture_exception()
            return False

    def leave(self, profile: Profile) -> bool:
        """Remove profile from a group."""
        try:
            self.group.profiles.remove(profile)
            self.group.save()
            return True
        except (AttributeError, IntegrityError, ValueError):
            capture_exception()
            return False

    def make_admin(self, admin_profile: Profile, profile_uuid: str) -> bool:
        """Make profile a group admin."""
        if admin_profile not in self.group.admins:
            raise UserValidationFailedException('Only admins are allowed to create admins.')

        try:
            profile = Profile.objects.get(uuid=profile_uuid)

            self.group.profiles.remove(profile)
            self.group.save()
            return True
        except (AttributeError, IntegrityError, ValueError):
            capture_exception()
            return False
