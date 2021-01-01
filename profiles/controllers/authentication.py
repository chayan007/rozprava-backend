from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from profiles.models import Profile


class Authenticator:

    @staticmethod
    def register(**kwargs):
        first_name = kwargs.get('first_name')
        last_name = kwargs.get('last_name')
        username = kwargs.get('username')
        password = kwargs.get('password')
        email = kwargs.get('email')
        try:
            user_obj = User.objects.create_user(username, email, password)
        except BaseException:
            return None, {'error': 'Username already exists.'}
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.save()
        Profile.objects.create(user=user_obj)
        user = authenticate(username=username, password=password)
        if not user:
            return None, {'error': 'Username/Password is incorrect.'}
        return user, {}

    def initiate_reset_password(self, user):
        pass

    def reset_password(self, username, reset_token, password):
        pass