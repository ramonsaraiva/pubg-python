from . import exceptions
from .clients import (
    APIClient,
    TelemetryClient,
)
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

    def samples(self):
        return self.endpoint('samples')

    def telemetry(self, url):
        data = self.telemetry_client.request(url)
        return Telemetry(data, url)
