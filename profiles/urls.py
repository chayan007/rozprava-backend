from django.urls import path, include

from profiles.controllers.social.facebook_login import FacebookLogin
from profiles.controllers.social.twitter_login import TwitterLogin

urlpatterns = [
    path(r'^social-auth/', include('rest_auth.urls')),
    path(r'^social-auth/registration/', include('rest_auth.registration.urls')),
    path(r'^social-auth/facebook/$', FacebookLogin.as_view(), name='fb_login'),
    path(r'^social-auth/twitter/$', TwitterLogin.as_view(), name='twitter_login'),
]
