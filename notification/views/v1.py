from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from notification.controllers.notification_handler import NotificationHandler
from notification.serializers import NotificationSerializer


class NotificationView(ListAPIView):
    """Handle notifications for profile."""

    serializer_class = NotificationSerializer
    permission_class = (IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        """Retrieve list of notifications for an user."""
        notifications = NotificationHandler(
            request.user.profile.uuid
        ).get(
            request.query_params.get('notification_type')
        )
        serialized_notifications = self.serializer_class(notifications, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data=serialized_notifications.data
        )

    def post(self, request, *args, **kwargs):
        """Mark all notifications read."""
        notification_uuids = request.data.get('notification_uuids')
        if not notification_uuids:
            raise ValueError('`notification_uuids` (type: Array) cannot be empty.')
        is_done = NotificationHandler(
            self.request.user.profile.uuid
        ).mark_read(notification_uuids)
        return Response(
            status=status.HTTP_202_ACCEPTED,
            data={
                'message': 'All notifications are marked read!',
                'is_completed': is_done
            }
        )
