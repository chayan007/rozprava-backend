from django.contrib.auth.models import User

from profiles.models import FollowerMap, Profile


class FollowerHandler:

    def __init__(self, user: User):
        self.profile = user.profile

    def follow(self, profile_uuid: str):
        """Follow/Unfollow an user."""
        following_profile = Profile.objects.get(uuid=profile_uuid)
        is_already_following = FollowerMap.objects.filter(
            follower=self.profile,
            following=following_profile
        ).first()
        if is_already_following:
            is_already_following.delete()
            return {'message': f'{is_already_following.following.user.username} has been unfollowed!'}
        FollowerMap.objects.create(
            follower=self.profile,
            following=following_profile
        )
        return {'message': f'{is_already_following.following.user.username} has been followed!'}
