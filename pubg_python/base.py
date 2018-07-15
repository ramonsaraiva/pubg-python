from . import exceptions
from .clients import (
    APIClient,
    TelemetryClient,
)
from .domain.base import Shard
from .domain.telemetry.base import Telemetry
from .querysets import QuerySet


def shardful_endpoint(f):
    def wrapper(self, *args, **kwargs):
        return QuerySet(self.api_client, self.shard_url.join(f.__name__))
    return wrapper


def endpoint(f):
    def wrapper(self, *args, **kwargs):
        return QuerySet(
            self.api_client, self.api_client.url.copy().join(f.__name__))
    return wrapper


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
        return self.api_client.url.copy().join(
            'shards/{}/'.format(self.shard.value))

    @shardful_endpoint
    def matches(self):
        pass

    @shardful_endpoint
    def players(self):
        pass

    @shardful_endpoint
    def samples(self):
        pass

    @endpoint
    def tournaments(self):
        return self.endpoint('tournaments')

    def telemetry(self, url):
        data = self.telemetry_client.request(url)
        return Telemetry(data, url)
