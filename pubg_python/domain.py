from enum import Enum


class Shard(Enum):
    PC_AS = 'pc-as'  # Asia
    PC_EU = 'pc-eu'  # Europe
    PC_KAKAO = 'pc-kakao'  # Kakaogames server (Korea only)
    PC_KRJP = 'pc-krjp'  # Korea/Japan
    PC_NA = 'pc-na'  # North America
    PC_OC = 'pc-oc'  # Oceania
    PC_SA = 'pc-sa'  # South and Central America
    PC_SEA = 'pc-sea'  # South East Asia
    XBOX_AS = 'xbox-as'  # Asia
    XBOX_EU = 'xbox-eu'  # Europe
    XBOX_NA = 'xbox-na'  # North America
    XBOX_OC = 'xbox-oc'  # Oceania


class Filter(Enum):
    CREATED_AT_START = 'createdAt-start'
    CREATED_AT_END = 'createdAt-end'
    PLAYER_IDS = 'playerIds'
    GAME_MODE = 'gameMode'


class GameMode(Enum):
    SOLO = 'solo'
    SQUAD = 'squad'


class Domain:

    def __init__(self, data):
        self._data = data
        self.from_json()

    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.__name__, self.id)

    def __str__(self):
        return self.id

    def from_json(self):
        self.id = self._data.get('id')


class Match(Domain):

    def from_json(self):
        super().from_json()
        self.created_at = self._data.get('createdAt')
        self.duration = self._data.get('duration')
        self.rounds = self._data.get('rounds')
        self.spectators = self._data.get('spectators')
        self.stats = self._data.get('stats')
        self.game_mode = self._data.get('gameMode')
        self.patch_version = self._data.get('patchVersion')
        self.title_id = self._data.get('titleId')
        self.shard_id = self._data.get('shardId')
        self.tags = self._data.get('tags')

        self.rosters = self.parse_rosters()
        self.assets = self.parse_assets()

    def parse_rosters(self):
        return [Roster(data) for data in self._data.get('rosters')]

    def parse_assets(self):
        return [Asset(data) for data in self._data.get('assets')]


class Roster(Domain):

    def from_json(self):
        super().from_json()
        self.team = self._data.get('team')
        self.stats = self._data.get('stats')
        self.won = self._data.get('won')
        self.shard_id = self._data.get('shardId')

        self.participants = self.parse_participants()

    def parse_participants(self):
        return [Participant(data) for data in self._data.get('participants')]


class Participant(Domain):

    def from_json(self):
        super().from_json()
        self.stats = self._data.get('stats')
        self.actor = self._data.get('actor')
        self.shard_id = self._data.get('shardId')


class Asset(Domain):

    def from_json(self):
        super().from_json()
        self.title_id = self._data.get('titleId')
        self.shard_id = self._data.get('shardId')
        self.name = self._data.get('name')
        self.description = self._data.get('description')
        self.created_at = self._data.get('createdAt')
        self.filename = self._data.get('filename')
        self.content_type = self._data.get('contentType')
        self.url = self._data.get('url')
