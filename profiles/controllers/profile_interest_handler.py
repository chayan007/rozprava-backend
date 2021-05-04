from django.db import IntegrityError

from profiles.models import Profile, ProfileInterest


class ProfileInterestHandler:
    """Handle e2e functionalities for user interests."""

    def __init__(self, profile: Profile):
        self.profile = profile

    def add(self, categories: [int]):
        """Add category to profile interest."""
        for category in categories:
            try:
                ProfileInterest.objects.create(
                    profile=self.profile,
                    category=category
                )
            except (AttributeError, IntegrityError, ValueError):
                continue

    def remove(self, categories: [int]):
        """Remove category from profile interest."""
        for category in categories:
            try:
                profile_interest = ProfileInterest.objects.get(
                    profile=self.profile,
                    category=category
                )
                profile_interest.is_deleted = True
                profile_interest.save()
            except (AttributeError, IntegrityError, ValueError):
                continue
