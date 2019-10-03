from . import exceptions
from .clients import (
    APIClient,
    TelemetryClient,
)
from .domain.base import Shard
from .domain.telemetry.base import Telemetry
from .exceptions import RequiredFilterError
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
        pass

    def seasons(self, season_id=None, **kwargs):
        # TODO: probably redesign this?
        if season_id is None:
            return QuerySet(self.api_client, self.shard_url.join('seasons'))

        game_mode = kwargs.pop('game_mode', None)
        player_id = kwargs.pop('player_id', None)

        if game_mode is None and player_id is None:
            raise RequiredFilterError(
                'game_mode or player_id is required for fetching seasons.')

        if game_mode is not None:
            return QuerySet(self.api_client, self.shard_url.join(
               'seasons/{}/gameMode/{}/players'.format(season_id, game_mode)))
        if player_id is not None:
            return QuerySet(self.api_client, self.shard_url.join(
               'players/{}/seasons/{}'.format(player_id, season_id)))

    def leaderboards(self, game_mode):
        return QuerySet(self.api_client, self.shard_url.join(
            'leaderboards/{}'.format(game_mode)))

    def weapon_mastery(self, player_id):
        return QuerySet(self.api_client, self.shard_url.join(
            'players/{}/weapon_mastery'.format(player_id)))

    def telemetry(self, url):
        data = self.telemetry_client.request(url)
        return Telemetry(data, url)
