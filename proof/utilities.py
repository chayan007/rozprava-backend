import datetime
import random


def get_proof_upload_path(obj, filename: str):
    return 'proof/{}/{}/{}_{}'.format(
        obj.profile.user.username,
        datetime.date.today().strftime('%d_%B_%Y'),
        str(random.randint(1, 9999)),
        filename
    )
