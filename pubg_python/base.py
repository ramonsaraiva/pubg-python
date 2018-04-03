import json

import furl
import requests

from . import exceptions
from .decorators import requires_shard
from .domain import Shard
from .querysets import QuerySet


class PUBG:

    def __init__(self, api_key, shard=None):
        self.shard = shard
        self.client = Client(api_key)

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
        url = self.client.url.copy()
        url.path = 'shards/{}'.format(self.shard.value)
        return url

    @requires_shard
    def endpoint(self, name):
        url = self.shard_url
        url.path.segments.append(name)
        return QuerySet(self.client, url)

    def matches(self):
        return self.endpoint('matches')

    def players(self):
        return self.endpoint('players')


class Client:

    BASE_URL = 'https://api.playbattlegrounds.com/'

    def __init__(self, api_key):
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': api_key,
            'Accept': 'application/vnd.api+json'
        })
        self.url = furl.furl(self.BASE_URL)

    API_OK = 200
    API_ERRORS_MAPPING = {
        401: exceptions.UnauthorizedError,
        404: exceptions.NotFoundError,
        415: exceptions.InvalidContentTypeError,
        429: exceptions.RateLimitError,
    }

    def request(self, endpoint):
        response = self.session.get(endpoint)

        if response.status_code != self.API_OK:
            exception = self.API_ERRORS_MAPPING.get(
                response.status_code, exceptions.APIError)
            raise exception()

        return json.loads(response.text)
