import random


def get_profile_verification_image_upload_path(obj, filename: str):
    return 'verification/{}/{}/{}'.format(
        obj.identity_type,
        obj.profile.user.username,
        filename
    )


def get_profile_dp_image_upload_path(obj, filename: str):
    return 'verification/{}/{}_{}'.format(
        obj.user.username,
        str(random.randint(1, 9999)),
        filename
    )
