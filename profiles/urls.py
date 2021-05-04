from django.urls import path, include

from profiles.controllers.social.facebook_login import FacebookLogin
from profiles.controllers.social.twitter_login import TwitterLogin
from profiles.views.v1 import (
    PasswordUpdateView,
    ProfileListView,
    ProfileUpdateView,
    ProfileView,
    GroupView,
    GroupSearchView,
    GroupDeleteView,
    JoinGroupView,
    LeaveGroupView,
    GroupAdminChangeView,
    ProfileInterestView
)

urlpatterns = [
    # Functional Views
    path('social-auth/', include('rest_auth.urls')),
    path('social-auth/registration/', include('rest_auth.registration.urls')),
    path('social-auth/facebook/', FacebookLogin.as_view(), name='fb-login'),
    path('social-auth/twitter/', TwitterLogin.as_view(), name='twitter-login'),

    # Class Based Views
    path('list/', ProfileListView.as_view(), name='list'),
    path('password/reset/', PasswordUpdateView.as_view(), name='password-reset'),
    path('update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('interests/', ProfileInterestView.as_view(), name='profile-interest'),
    path('group/', GroupView.as_view(), name='group'),
    path('group/search/<group_uuid: str>', GroupSearchView.as_view(), name='group-search'),
    path('group/delete/<group_uuid: str>', GroupDeleteView.as_view(), name='group-delete'),
    path('group/join/<group_uuid: str>', JoinGroupView.as_view(), name='group-delete'),
    path('group/leave/<group_uuid: str>', LeaveGroupView.as_view(), name='group-delete'),
    path('group/admin/<group_uuid: str>', GroupAdminChangeView.as_view(), name='group-delete'),
    path('group/admin/<group_uuid: str>', GroupAdminChangeView.as_view(), name='group-delete'),
    path('<username>/', ProfileView.as_view(), name='profile-detail')
]
