from django.urls import path, include

from proof.views.v1 import (
    DebateProofListView,
    DebateProofView,
    CaseProofListView,
    CaseProofView
)


urlpatterns = [
    # Class Based Views
    path('v1/', include([
        path('debate/list/', DebateProofListView.as_view(), name='debate-list'),
        path('case/list/', CaseProofListView.as_view(), name='case-list'),
        path('case/<case_slug>/', CaseProofView.as_view(), name='case'),
        path('debate/', DebateProofView.as_view(), name='debate')
    ]))
]
