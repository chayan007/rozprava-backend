from django.contrib.auth.models import User

from profiles.models import FollowerMap, Profile


class FollowerHandler:

    def __init__(self, user: User):
        self.profile = user.profile

    def is_already_following(self, profile_uuid: str):
        """Check if authenticated user is already following another user."""
        return FollowerMap.objects.filter(
            follower=self.profile,
            following__uuid=profile_uuid
        ).exists()

    def follow(self, profile_username: str):
        """Follow/Unfollow an user."""
        following_profile = Profile.objects.get(user__username=profile_username)
        is_already_following = FollowerMap.objects.filter(
            follower=self.profile,
            following=following_profile
        ).first()
        if is_already_following:
            is_already_following.delete()
            return {'message': f'{is_already_following.following.user.username} has been unfollowed!'}
        is_already_following = FollowerMap.objects.create(
            follower=self.profile,
            following=following_profile
        )
        return {'message': f'{is_already_following.following.user.username} has been followed!'}
