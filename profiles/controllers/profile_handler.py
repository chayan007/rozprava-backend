from sentry_sdk import capture_exception

from profiles.models import Profile


class ProfileHandler:

    NON_UPDATABLE_FIELDS = [
        'celebrity_rank',
        'is_celebrity',
        'is_verified'
    ]

    USER_FIELDS = [
        'first_name',
        'last_name',
        'username'
    ]

    def __init__(self, profile_uuid: str):
        self.profile = Profile.objects.get(uuid=profile_uuid)

    def update_details(self, updated_details: dict):
        """Edit profile object attributes."""
        for attribute, value in updated_details.items():
            if attribute in self.NON_UPDATABLE_FIELDS or not value:
                continue

            if attribute == 'password':
                self.profile.user.set_password(value)
                self.profile.user.save()
                continue

            if attribute in self.USER_FIELDS:
                setattr(self.profile.user, attribute, value)
                self.profile.user.save()
            else:
                setattr(self.profile, attribute, value)
        try:
            self.profile.save()
            return self.profile
        except (AttributeError, ValueError):
            capture_exception()
            return False
