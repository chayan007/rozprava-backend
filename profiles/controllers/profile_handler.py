from profiles.models import Profile


class ProfileHandler:

    NON_UPDATABLE_FIELDS = [
        'celebrity_rank',
        'is_celebrity',
        'is_verified'
    ]

    def __init__(self, profile_uuid: str):
        self.profile = Profile.objects.get(uuid=profile_uuid)

    def update_details(self, updated_details: dict):
        """Edit profile object attributes."""
        for attribute, value in updated_details.items():
            if attribute in self.NON_UPDATABLE_FIELDS:
                continue
            setattr(self.profile, attribute, value)
        try:
            self.profile.save()
            return True
        except (AttributeError, ValueError):
            print(f'Could not update {self.profile.user.username}')
            return False
