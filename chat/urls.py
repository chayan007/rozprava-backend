from django.urls import path

from case.views.v1 import (
    CaseActivityView,
    CaseDetailView,
    CaseListView
)

urlpatterns = [
    # Class Based Views
    path('list/', CaseListView.as_view(), name='list'),
    path('activity/<case_uuid>/<activity_type>', CaseActivityView.as_view(), name='activity'),
    path('detail/<slug>/', CaseDetailView.as_view(), name='detail'),
]
