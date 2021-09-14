from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.conf.urls import url

from chat.websocket.consumers.chat_consumer import ChatConsumer

websocket_urlpatterns = [
    url(r'^ws/chat/(?P<room_name>\w+)/$', ChatConsumer),
]

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})
