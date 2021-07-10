import random


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
