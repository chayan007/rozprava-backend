from django.contrib.gis.geoip2 import GeoIP2

from profiles.models import Profile

from tracker.models import Location


class LocationHandler:

    def __init__(self, profile_uuid=None):
        self.geo_location = GeoIP2()
        self.profile = Profile.objects.get(uuid=profile_uuid) if profile_uuid else None

    def get_location(self, ip_address):
        """Get location from the IP address."""
        try:
            create_queryset = {
                'ip_address': ip_address,
                'country': self.geo_location.country(ip_address),
                'city': self.geo_location.city(ip_address),
                'coordinates': self.geo_location.lat_lon(ip_address)
            }
            if self.profile:
                create_queryset['profile'] = self.profile
            return Location.objects.create(**create_queryset)
        except BaseException:
            return None
