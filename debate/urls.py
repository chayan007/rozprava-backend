from django.urls import path, include

from debate.views.v1 import (
    DebateView,
    DebateActivityView,
    DebateListView,
    RebuttalView
)

urlpatterns = [
    # Class Based Views
    path('v1/', include([
        path('list/', DebateListView.as_view(), name='list'),
        path('activity/<debate_uuid>/<activity_type>', DebateActivityView.as_view(), name='activity'),
        path('detail/<debate_uuid>/', DebateView.as_view(), name='detail'),
        path('rebuttal/detail/<slug>/', RebuttalView.as_view(), name='rebuttal-detail'),
    ])),
]
