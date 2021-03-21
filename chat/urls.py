from django.urls import path, include

from chat.views.v1 import (
    ChatMenuView,
    ChatView
)

urlpatterns = [
    # Class Based Views
    path('v1/', include([
        path('menu/', ChatMenuView.as_view(), name='menu'),
        path('messaging/<sender_uuid>/', ChatView.as_view(), name='messaging'),
    ])),
]
