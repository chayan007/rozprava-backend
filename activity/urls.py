from django.urls import path, include

from activity.views.v1 import ActivityListView

urlpatterns = [
    # Class Based Views
    path('v1/', include([
        path('list/', ActivityListView.as_view(), name='list')
    ])),
]
