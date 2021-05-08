from django.urls import path, include

from case.views.v1 import (
    CaseActivityView,
    CaseListView,
    CaseView
)

urlpatterns = [
    # Class Based Views
    path('v1/', include([
        path('list/', CaseListView.as_view(), name='list'),
        path('activity/<case_uuid>/<activity_type>', CaseActivityView.as_view(), name='activity'),
        path('create/', CaseView.as_view(), name='create'),
        path('<slug>/', CaseView.as_view(), name='detail'),
    ]))
]
