from django.urls import path, include

from case.views.v1 import (
    CaseActivityView,
    CaseCreateView,
    CaseListView,
    CaseView
)

urlpatterns = [
    # Class Based Views
    path('v1/', include([
        path('list/', CaseListView.as_view(), name='list'),
        path('activity/<case_uuid>/<activity_type>', CaseActivityView.as_view(), name='activity'),
        path('create/', CaseCreateView.as_view(), name='create'),
        path('<slug>/', CaseView.as_view(), name='detail'),
    ]))
]
