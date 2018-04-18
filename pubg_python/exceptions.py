class InvalidShardError(Exception):
    pass


class ShardNotDefinedError(Exception):
    pass


class InvalidFilterError(Exception):
    pass


class APIError(Exception):

    def __init__(self, message='Something went wrong with your request'):
        super(APIError, self).__init__(message)


class ResponseError(APIError):
    pass


class UnauthorizedError(APIError):

    def __init__(self):
        super(UnauthorizedError, self).__init__('API key invalid or missing')


class NotFoundError(APIError):

    def __init__(self):
        super(NotFoundError, self).__init__('The specified resource was not found')


class InvalidContentTypeError(APIError):

    def __init__(self):
        super(InvalidContentTypeError, self).__init__('Unsupported media type')


class RateLimitError(APIError):

    def __init__(self):
        super(RateLimitError, self).__init__('Too many requests')
