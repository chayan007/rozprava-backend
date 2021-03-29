from django.urls import include, path

from notification.views.v1 import NotificationView

urlpatterns = [
    # Class Based Views
    path('v1/', include([
        path('', NotificationView.as_view(), name='list')
    ])),
]
