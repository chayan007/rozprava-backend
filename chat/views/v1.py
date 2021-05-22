from rest_framework import status
from rest_framework.generics import ListAPIView, GenericAPIView
from rest_framework.response import Response

from chat.controllers.o2o_chat_engine import OneToOneChatEngine
from chat.serializers import OneToOneMessageSerializer
from profiles.serializers import ProfileSerializer


class ChatView(GenericAPIView):
    """Chat view for users."""

    serializer_class = OneToOneMessageSerializer

    def get(self, request, *args, **kwargs):
        receiver_uuid = request.user.profile.uuid
        sender_uuid = kwargs.get('sender_uuid')
        messaging_list = OneToOneChatEngine(
            sender_profile_uuid=sender_uuid,
            receiver_profile_uuid=receiver_uuid
        ).receive()
        serialized_messages = self.serializer_class(messaging_list, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data=serialized_messages
        )

    def post(self, request, *args, **kwargs):
        receiver_uuid = request.user.profile.uuid
        sender_uuid = kwargs.get('sender_uuid')
        is_message_sent = OneToOneChatEngine(
            sender_profile_uuid=sender_uuid,
            receiver_profile_uuid=receiver_uuid
        ).send(
            message=request.data.get('message'),
            media=request.data.get('media'),
        )
        return Response(
            status=status.HTTP_200_OK,
            data={
                'status': is_message_sent
            }
        )


class ChatMenuView(ListAPIView):
    """Perform operations on chat menu."""

    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        """Gets list of all messages from users."""
        receiver = request.user.profile
        messaging_list = OneToOneChatEngine(
            receiver_profile_uuid=receiver.uuid
        ).show_messaging_list()
        serialized_messaging_list = self.serializer_class(messaging_list, many=True)
        return Response(
            data=serialized_messaging_list.data,
            status=status.HTTP_200_OK
        )

    def delete(self, request, *args, **kwargs):
        """Deletes all messages of an user."""
        pass
