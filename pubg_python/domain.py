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

    def __init__(self, data, meta=None):
        self._raw_data = data
        self._meta = meta or Meta(self._raw_data)
        self._data = self._raw_data['data']
        self.from_json()

        self.process_relationships()

    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.__name__, self.id)

    def __str__(self):
        return str(self.id)

    @classmethod
    def instance(cls, data, meta=None):
        return globals()[data['data']['type'].title()](data, meta)

    def from_json(self):
        self.id = self._data.get('id')
        self.type = self._data.get('type')
        self.attributes = self._data.get('attributes', {})
        self.relationships = self._data.get('relationships', {})

    def process_relationships(self):
        if not self.relationships:
            return

        for name, relationship in self.relationships.items():
            if not relationship['data']:
                continue

            setattr(self, name, [])
            rel = getattr(self, name)
            for data in relationship['data']:
                item = self._meta.retrieve(data)
                rel.append(Domain.instance({'data': item}, meta=self._meta))


class Meta:

    def __init__(self, data):
        self._meta = data.get('meta')
        self._links = data.get('links')
        self._included = data.get('included')

    @property
    def meta(self):
        return self._meta

    @property
    def links(self):
        return self._links

    @property
    def included(self):
        return self._included

    def retrieve(self, data):
        if not self.included:
            return data
        return next(
            filter(lambda x: x['id'] == data['id'], self.included), data)


class Match(Domain):

    def from_json(self):
        super().from_json()
        self.created_at = self.attributes.get('createdAt')
        self.duration = self.attributes.get('duration')
        self.stats = self.attributes.get('stats')
        self.game_mode = self.attributes.get('gameMode')
        self.patch_version = self.attributes.get('patchVersion')
        self.title_id = self.attributes.get('titleId')
        self.shard_id = self.attributes.get('shardId')
        self.tags = self.attributes.get('tags')


class Roster(Domain):

    def from_json(self):
        super().from_json()
        self.shard_id = self.attributes.get('shardId')
        self.stats = self.attributes.get('stats')
        self.won = self.attributes.get('won')


class Participant(Domain):

    def from_json(self):
        super().from_json()
        self.actor = self.attributes.get('actor')
        self.shard_id = self.attributes.get('shardId')
        self.stats = self.attributes.get('stats')
        self.unpack_stats()

    def unpack_stats(self):
        self.dbnos = self.stats.get('DBNOs')
        self.assists = self.stats.get('assists')
        self.boosts = self.stats.get('boosts')
        self.damage_dealt = self.stats.get('damageDealt')
        self.death_type = self.stats.get('deathType')
        self.headshot_kills = self.stats.get('headshotKills')
        self.heals = self.stats.get('heals')
        self.kill_place = self.stats.get('killPlace')
        self.kill_points_delta = self.stats.get('killPointsDelta')
        self.kill_streaks = self.stats.get('killStreaks')
        self.kills = self.stats.get('kills')
        self.last_kill_points = self.stats.get('lastKillPoints')
        self.last_win_points = self.stats.get('lastWinPoints')
        self.longest_kill = self.stats.get('longestKill')
        self.most_damage = self.stats.get('mostDamage')
        self.name = self.stats.get('name')
        self.player_id = self.stats.get('playerId')
        self.revives = self.stats.get('revives')
        self.ride_distance = self.stats.get('rideDistance')
        self.road_kills = self.stats.get('roadKills')
        self.team_kills = self.stats.get('teamKills')
        self.time_survived = self.stats.get('timeSurvived')
        self.vehicle_destroys = self.stats.get('vehicleDestroys')
        self.walk_distance = self.stats.get('walkDistance')
        self.weapons_acquired = self.stats.get('weaponsAcquired')
        self.win_place = self.stats.get('winPlace')
        self.win_points_delta = self.stats.get('winPointsDelta')


class Asset(Domain):

    def from_json(self):
        super().from_json()
        self.url = self.attributes.get('URL')
        self.created_at = self.attributes.get('createdAt')
        self.description = self.attributes.get('description')
        self.name = self.attributes.get('name')


class Player(Domain):

    def from_json(self):
        super().from_json()
        self.created_at = self.attributes.get('createdAt')
        self.name = self.attributes.get('name')
        self.patch_version = self.attributes.get('patchVersion')
        self.shard_id = self.attributes.get('shardId')
        self.stats = self.attributes.get('stats')
        self.title_id = self.attributes.get('titleId')
        self.updated_at = self.attributes.get('updated_at')
