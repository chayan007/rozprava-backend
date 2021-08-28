from django.urls import path, include

from profiles.controllers.social.facebook_login import FacebookLogin
from profiles.controllers.social.google_login import GoogleLogin
from profiles.controllers.social.twitter_login import TwitterLogin
from profiles.views.v1 import (
    PasswordUpdateView,
    ProfileSearchView,
    ProfileUpdateView,
    ProfileView,
    GroupView,
    GroupSearchView,
    GroupDeleteView,
    JoinGroupView,
    LeaveGroupView,
    GroupAdminChangeView,
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
    path('search/<search_username>', ProfileSearchView.as_view(), name='list'),
    path('password/reset/', PasswordUpdateView.as_view(), name='password-reset'),
    path('update/', ProfileUpdateView.as_view(), name='profile-update'),

    path('interests/', ProfileInterestView.as_view(), name='profile-interest'),
    path('recommend/', RecommendProfileView.as_view(), name='profile-recommendation'),

    path('group/', GroupView.as_view(), name='group'),
    path('group/search/<group_uuid>', GroupSearchView.as_view(), name='group-search'),
    path('group/delete/<group_uuid>', GroupDeleteView.as_view(), name='group-delete'),
    path('group/join/<group_uuid>', JoinGroupView.as_view(), name='group-delete'),
    path('group/leave/<group_uuid>', LeaveGroupView.as_view(), name='group-delete'),
    path('group/admin/<group_uuid>', GroupAdminChangeView.as_view(), name='group-delete'),
    path('group/admin/<group_uuid>', GroupAdminChangeView.as_view(), name='group-delete'),

    path('user/<user_string>/', ProfileView.as_view(), name='profile-detail'),

    # Reset Password APIs
    path('reset-password/check-user/<user_string>/', ResetPasswordCheckUserView.as_view(), name='check-user'),
    path('reset-password/send-otp/<username>/', ResetPasswordSendOTPView.as_view(), name='send-otp'),
    path('reset-password/verify-otp/<username>/<int:otp>/', ResetPasswordVerifyOTPView.as_view(), name='verify-otp'),
    path('reset-password/change-password/<username>/', ResetPasswordView.as_view(), name='change-password'),
]
