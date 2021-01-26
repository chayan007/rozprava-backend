import datetime


def get_profile_verification_image_upload_path(obj, filename: str):
    return 'verification/{}/{}/{}'.format(
        obj.identity_type,
        obj.profile.user.username,
        filename
    )
