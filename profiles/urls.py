from django.urls import path, include

from profiles.controllers.social.facebook_login import FacebookLogin
from profiles.controllers.social.google_login import GoogleLogin
from profiles.controllers.social.twitter_login import TwitterLogin
from profiles.views.v1 import (
    PasswordUpdateView,
    ProfileSearchView,
    ProfileUpdateView,
    ProfileView,
    FollowerListView,
    GroupView,
    GroupCreateView,
    GroupSearchView,
    GroupDeleteView,
    GroupListView,
    JoinGroupView,
    LeaveGroupView,
    GroupAdminChangeView,
    ProfileFollowView,
    ProfileInterestView,
    RecommendProfileView,
    ResetPasswordView,
    ResetPasswordCheckUserView,
    ResetPasswordSendOTPView,
    ResetPasswordVerifyOTPView
)

urlpatterns = [
    # Functional Views
    path('auth/', include('rest_auth.urls')),
    path('auth/registration/', include('rest_auth.registration.urls')),
    path('social-auth/facebook/', FacebookLogin.as_view(), name='fb-login'),
    path('social-auth/twitter/', TwitterLogin.as_view(), name='twitter-login'),
    path('social-auth/google/', GoogleLogin.as_view(), name='google-login'),

    # Class Based Views
    path('search/<username>', ProfileSearchView.as_view(), name='list'),
    path('followers/<int:is_followers_required>', ProfileSearchView.as_view(), name='list'),
    path('password/reset/', PasswordUpdateView.as_view(), name='password-reset'),
    path('update/', ProfileUpdateView.as_view(), name='profile-update'),

    path('interests/', ProfileInterestView.as_view(), name='profile-interest'),
    path('recommend/', RecommendProfileView.as_view(), name='profile-recommendation'),
    path('follow/<following_username>', ProfileFollowView.as_view(), name='profile-follow'),
    path('follower/<username>', FollowerListView.as_view(), name='follower-list'),

    path('groups/', GroupListView.as_view(), name='group-list'),
    path('group/', GroupCreateView.as_view(), name='group-create'),
    path('group/<group_uuid>/', GroupView.as_view(), name='group'),
    path('group/search/<group_name>', GroupSearchView.as_view(), name='group-search'),
    path('group/delete/<group_uuid>', GroupDeleteView.as_view(), name='group-delete'),
    path('group/join/<group_uuid>', JoinGroupView.as_view(), name='group-delete'),
    path('group/leave/<group_uuid>', LeaveGroupView.as_view(), name='group-leave'),
    path('group/admin/<group_uuid>', GroupAdminChangeView.as_view(), name='group-admin'),

    path('user/<user_string>/', ProfileView.as_view(), name='profile-detail'),

    # Reset Password APIs
    path('reset-password/check-user/<user_string>/', ResetPasswordCheckUserView.as_view(), name='check-user'),
    path('reset-password/send-otp/<username>/', ResetPasswordSendOTPView.as_view(), name='send-otp'),
    path('reset-password/verify-otp/<username>/<int:otp>/', ResetPasswordVerifyOTPView.as_view(), name='verify-otp'),
    path('reset-password/change-password/<username>/', ResetPasswordView.as_view(), name='change-password'),
]
