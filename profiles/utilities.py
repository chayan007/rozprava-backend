import random

from case.models import Case

from profiles.models import FollowerMap, Profile


def get_profile_verification_image_upload_path(obj, filename: str) -> str:
    return 'verification/{}/{}/{}'.format(
        obj.identity_type,
        obj.profile.user.username,
        filename
    )


def get_profile_dp_image_upload_path(obj, filename: str) -> str:
    return 'verification/{}/{}_{}'.format(
        obj.user.username,
        str(random.randint(1, 9999)),
        filename
    )


def check_if_request_authenticated(request) -> bool:
    return (
        request and
        getattr(request, 'user', None) and
        getattr(request.user, 'profile', None)
    )


def get_profile_metrics(profile: Profile) -> dict:
    return {
        'posts': Case.objects.filter(profile=profile).count(),
        'followers': FollowerMap.objects.filter(following=profile).count(),
        'following': FollowerMap.objects.filter(follower=profile).count()
    }
