import datetime
import os

from rest_framework import status
from rest_framework.response import Response


class InternalSecurityMiddleware:

    DATETIME_FORMAT = 'DDMMYYhh'
    API_ROUTE_PATH = '/v1/'
    PROFILE_API_PREFIX = '/profile/'
    SECURITY_HEADER = 'X-Security-Key'

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f'Request :: [{request.path}]', getattr(request, 'data', {}))
        current_timestamp = datetime.datetime.now().strftime(self.DATETIME_FORMAT)

        if not os.getenv('DJANGO_SETTINGS_MODULE') == 'settings.local':
            headers = request.headers
            path = request.path

            if (
                self.API_ROUTE_PATH in path or
                path.startswith(self.PROFILE_API_PREFIX)
            ):
                security_header = headers.get(self.SECURITY_HEADER)
                if security_header:
                    first_timestamp = security_header[0:9]
                    last_timestamp = security_header[-8:][::-1]
                    if not first_timestamp == last_timestamp == current_timestamp:
                        return Response(
                            data={'error': 'Security Token missing.'},
                            status=status.HTTP_401_UNAUTHORIZED
                        )
                else:
                    return Response(
                        data={'error': 'Security Token missing.'},
                        status=status.HTTP_401_UNAUTHORIZED
                    )

        try:
            response = self.get_response(request)
        except BaseException:
            response = Response(
                data={'error': 'Something happened at our end. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        print('Response :: ', getattr(response, 'data', 'No data found in response.'), '\n\n')
        return response
