from datetime import datetime


class InvalidShardError(Exception):
    pass


class InvalidFilterError(Exception):
    pass


class RequiredFilterError(Exception):
    pass


class APIError(Exception):

    def __init__(self, message='Something went wrong with your request',
                 *args, **kwargs):
        super().__init__(message)


class ResponseError(APIError):
    pass


class UnauthorizedError(APIError):

    def __init__(self, *args, **kwargs):
        super().__init__('API key invalid or missing')


class NotFoundError(APIError):

    def __init__(self, *args, **kwargs):
        super().__init__('The specified resource was not found')


class InvalidContentTypeError(APIError):

    def __init__(self, *args, **kwargs):
        super().__init__('Unsupported media type')


class RateLimitError(APIError):

    def __init__(self, *args, **kwargs):
        self.response_headers = kwargs.pop('response_headers', None)
        self.rl_limit = int(self.response_headers.get('X-Ratelimit-Limit'))
        self.rl_reset = datetime.fromtimestamp(
                int(self.response_headers.get('X-Ratelimit-Reset')))
        super().__init__('Too many requests. Limit: {} Reset: {}'.format(
           self.rl_limit, self.rl_reset))


class OldTelemetryError(APIError):

    def __init__(self, *args, **kwargs):
        super().__init__('Telemetry was not found or no longer available')


class TelemetryURLError(APIError):

    def __init__(self, *args, **kwargs):
        super().__init__('Telemetry host differs from official')
