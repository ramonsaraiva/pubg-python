import json

import furl
import requests

from . import exceptions
from .decorators import requires_shard
from .domain.base import Shard
from .domain.telemetry.base import Telemetry
from .querysets import QuerySet


class PUBG:

    def __init__(self, api_key, shard=None):
        self.shard = shard
        self.api_client = APIClient(api_key)
        self.telemetry_client = TelemetryClient()

    @property
    def shard(self):
        return self._shard

    @shard.setter
    def shard(self, value):
        if not isinstance(value, Shard):
            raise exceptions.InvalidShardError('Invalid Shard')
        self._shard = value

    @property
    def shard_url(self):
        url = self.api_client.url.copy()
        url.path = 'shards/{}'.format(self.shard.value)
        return url

    @requires_shard
    def endpoint(self, name):
        url = self.shard_url
        url.path.segments.append(name)
        return QuerySet(self.api_client, url)

    def matches(self):
        return self.endpoint('matches')

    def players(self):
        return self.endpoint('players')

    def telemetry(self, url):
        data = self.telemetry_client.request(url)
        return Telemetry(data)


class Client:

    API_OK = 200
    API_ERRORS_MAPPING = {
        401: exceptions.UnauthorizedError,
        404: exceptions.NotFoundError,
        415: exceptions.InvalidContentTypeError,
        429: exceptions.RateLimitError,
    }

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'Accept': 'application/vnd.api+json'})
        self.url = furl.furl()

    def request(self, endpoint):
        response = self.session.get(endpoint)

        if response.status_code != self.API_OK:
            exception = self.API_ERRORS_MAPPING.get(
                response.status_code, exceptions.APIError)
            raise exception()

        return json.loads(response.text)


class APIClient(Client):

    BASE_URL = 'https://api.playbattlegrounds.com/'

    def __init__(self, api_key):
        super().__init__()
        self.session.headers.update({'Authorization': api_key})
        self.url.set(path=self.BASE_URL)


class TelemetryClient(Client):
    pass