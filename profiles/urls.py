from django.urls import path, include

from profiles.controllers.social.facebook_login import FacebookLogin
from profiles.controllers.social.twitter_login import TwitterLogin
from profiles.views.v1 import (
    PasswordUpdateView,
    ProfileListView,
    ProfileUpdateView,
    ProfileView
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
    path('profile/update/', ProfileUpdateView.as_view(), name='profile-update'),
    path('user/<username>/', ProfileView.as_view(), name='profile-detail'),
]
