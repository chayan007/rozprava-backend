import datetime


def get_proof_upload_path(obj, filename: str):
    return 'proof/{}/{}/{}'.format(
        obj.profile.user.username,
        datetime.date.today().strftime('%d_%B_%Y'),
        filename
    )
