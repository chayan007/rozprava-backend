from django.urls import path, include

from ads.views.v1 import CaseBoosterView


urlpatterns = [
    # Class Based Views
    path('v1/', include([
        path('<boost_uuid>/', CaseBoosterView.as_view(), name='update'),
        path('', CaseBoosterView.as_view(), name='create'),
    ])),
]
