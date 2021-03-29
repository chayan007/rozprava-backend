from notification.models import Notification
from profiles.models import Profile


class NotificationHandler:
    """Handle end to end user ops for notifications."""

    def __init__(self, profile_uuid: str):
        self.profile = Profile.records.filter(uuid=profile_uuid)

    def get(self, notification_label: str):
        """Get all notifications of specific label for the profile."""
        notifications = getattr(self, notification_label)
        return notifications

    @staticmethod
    def mark_read(notification_uuids: [str]):
        """Mark all notifications as read."""
        notification_objs = []
        for notification_uuid in notification_uuids:
            try:
                notification = Notification.records.get(uuid=notification_uuid)
                notification.is_read = True
                notification_objs.append(notification)
            except Notification.DoesNotExist:
                continue
        try:
            Notification.objects.bulk_update(notification_objs, ['is_read'])
            return True
        except (AttributeError, ValueError, Notification.DoesNotExist):
            return False

    def push(self):
        return Notification.objects.filter(
            profile=self.profile,
            type=Notification.NotificationType.PUSH.value
        ).order_by('-created_at')

    def sms(self):
        return Notification.objects.filter(
            profile=self.profile,
            type=Notification.NotificationType.SMS.value
        ).order_by('-created_at')

    def email(self):
        return Notification.objects.filter(
            profile=self.profile,
            type=Notification.NotificationType.EMAIL.value
        ).order_by('-created_at')

    def call(self):
        return Notification.objects.filter(
            profile=self.profile,
            type=Notification.NotificationType.CALL.value
        ).order_by('-created_at')
