from notification.models import Notification

from profiles.models import Profile


class NotificationInjector:
    """Handle entire end to end operations for notifications."""

    def __init__(self, profile_uuids: [str]):
        self.profiles = [
            Profile.objects.get(uuid=profile_uuid)
            for profile_uuid in profile_uuids
        ]

    def trigger(self, notification_label: str, message_id):
        """Triggers the notification kicking process."""
        message = message_id or None
        getattr(self, notification_label)(message)

    def push(self, message: str):
        notification_objs = []
        for profile in self.profiles:
            try:
                notification_objs.append(
                    Notification(profile=profile, message=message, type=Notification.NotificationType.PUSH.value)
                )
            except (AttributeError, ValueError):
                continue
        Notification.objects.bulk_create(notification_objs)

    def sms(self, message: str):
        notification_objs = []
        for profile in self.profiles:
            try:
                notification_objs.append(
                    Notification(profile=profile, message=message, type=Notification.NotificationType.SMS.value)
                )
            except (AttributeError, ValueError):
                continue
        Notification.objects.bulk_create(notification_objs)

    def email(self, message: str):
        notification_objs = []
        for profile in self.profiles:
            try:
                notification_objs.append(
                    Notification(profile=profile, message=message, type=Notification.NotificationType.EMAIL.value)
                )
            except (AttributeError, ValueError):
                continue
        Notification.objects.bulk_create(notification_objs)

    def call(self, message: str):
        notification_objs = []
        for profile in self.profiles:
            try:
                notification_objs.append(
                    Notification(profile=profile, message=message, type=Notification.NotificationType.CALL.value)
                )
            except (AttributeError, ValueError):
                continue
        Notification.objects.bulk_create(notification_objs)

    def all(self, message: str):
        notification_objs = []
        for profile in self.profiles:
            try:
                notification_objs.append(
                    Notification(profile=profile, message=message, type=Notification.NotificationType.ALL.value)
                )
            except (AttributeError, ValueError):
                continue
        Notification.objects.bulk_create(notification_objs)
