import requests

from django.contrib.gis.geoip2 import GeoIP2
from sentry_sdk import capture_exception

from profiles.models import Profile

from tracker.models import Location


class LocationHandler:

    URL = 'https://ipinfo.io/{}/json'

    def __init__(self, profile_uuid=None):
        self.profile = Profile.objects.get(uuid=profile_uuid) if profile_uuid else None

    def get_location(self, ip_address):
        """Get location from the IP address."""
        try:
            response = requests.get(self.URL.format(ip_address))
            assert response.status_code == 200
            geo_location = response.json()
            create_queryset = {
                'ip_address': ip_address,
                'country': geo_location.get('country'),
                'city': geo_location.get('city'),
                'coordinates': geo_location.get('loc')
            }
            if self.profile:
                create_queryset['profile'] = self.profile
            return Location.objects.create(**create_queryset)
        except BaseException:
            capture_exception()
            return
