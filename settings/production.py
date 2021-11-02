from settings.base import *

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '123',
            'secret': '456',
            'key': ''
        }
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'rozprava',
        'USER': 'rozprava',
        'PASSWORD': 'rozpravachayan',
        'HOST': 'rozprava.cbszzpzgor1e.ap-south-1.rds.amazonaws.com',
        'PORT': 5432
    }
}
