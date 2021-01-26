import datetime


def get_ads_image_upload_path(obj, filename: str):
    return 'ads/{}/images/{}/{}'.format(
        obj.name.replace(' ', '_'),
        datetime.date.today().strftime('%d_%B_%Y'),
        filename
    )


def get_ads_video_upload_path(obj, filename: str):
    return 'ads/{}/videos/{}/{}'.format(
        obj.name.replace(' ', '_'),
        datetime.date.today().strftime('%d_%B_%Y'),
        filename
    )
