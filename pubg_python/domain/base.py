import copy

from enum import Enum


class Shard(Enum):
    PC_AS = 'pc-as'  # Asia
    PC_EU = 'pc-eu'  # Europe
    PC_KAKAO = 'pc-kakao'  # Kakaogames server (Korea only)
    PC_KRJP = 'pc-krjp'  # Korea
    PC_NA = 'pc-na'  # North America
    PC_OC = 'pc-oc'  # Oceania
    PC_SA = 'pc-sa'  # South and Central America
    PC_SEA = 'pc-sea'  # South East Asia
    PC_JP = 'pc-jp'  # Japan
    PC_RU = 'pc-ru'  # Russia
    PC_TOURNAMENT = 'pc-tournament'  # PC Tournaments Shard
    XBOX_AS = 'xbox-as'  # Asia
    XBOX_EU = 'xbox-eu'  # Europe
    XBOX_NA = 'xbox-na'  # North America
    XBOX_OC = 'xbox-oc'  # Oceania
    XBOX_SA = 'xbox-sa'  # South America
    KAKAO = 'kakao'  # Kakao
    PSN = 'psn'  # PSN (Deprecated)
    STEAM = 'steam'  # Steam
    TOURNAMENT = 'tournament'  # Tournaments
    XBOX = 'xbox'  # Xbox (Deprecated)
    CONSOLE = 'console'  # Xbox/Psn


class Filter(Enum):
    CREATED_AT_START = 'createdAt-start'
    CREATED_AT_END = 'createdAt-end'
    PLAYER_IDS = 'playerIds'
    GAME_MODE = 'gameMode'


class Domain:

    def __init__(self, data, meta=None):
        self._raw_data = copy.deepcopy(data)
        raw_data = copy.deepcopy(data)
        self._meta = meta or Meta(raw_data)
        self._data = raw_data.pop('data', {})
        self.from_dict()

        self.process_relationships()

    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.__name__, self.id)

    def __str__(self):
        return str(self.id)

    @staticmethod
    def instance(data, meta=None):
        return globals()[data['data']['type'].title()](data, meta)

    def from_dict(self):
        self.description = self._data.get('description')
        self.id = self._data.get('id')
        self.type = self._data.get('type')
        self.attributes = self._data.pop('attributes', {})
        self.relationships = self._data.pop('relationships', {})

    def to_dict(self):
        return self._raw_data

    def process_relationships(self):
        if not self.relationships:
            return

        for name, relationship in self.relationships.items():
            if not relationship['data']:
                continue

            if isinstance(relationship['data'], list):
                setattr(self, name, [])
                rel = getattr(self, name)
                for data in relationship['data']:
                    item = self._meta.retrieve(data)
                    rel.append(
                        Domain.instance({'data': item}, meta=self._meta))

            elif isinstance(relationship['data'], dict):
                relationship_instance = Domain.instance(
                    relationship, meta=self._meta)
                setattr(self, name, relationship_instance)


class Meta:

    def __init__(self, data):
        self._meta = data.pop('meta', {})
        self._links = data.pop('links', {})
        self._included = data.pop('included', {})

    def retrieve(self, data):
        if not self._included:
            return data
        return next(
            filter(lambda x: x['id'] == data['id'], self._included), data)


class Sample(Domain):

    def from_dict(self):
        super().from_dict()
        self.created_at = self.attributes.get('createdAt')
        self.shard_id = self.attributes.get('shardId')
        self.title_id = self.attributes.get('titleId')


class Match(Domain):

    def from_dict(self):
        super().from_dict()
        self.created_at = self.attributes.get('createdAt')
        self.duration = self.attributes.get('duration')
        self.game_mode = self.attributes.get('gameMode')
        self.is_custom_match = self.attributes.get('isCustomMatch')
        self.map_name = self.attributes.get('mapName')
        self.patch_version = self.attributes.get('patchVersion')
        self.shard_id = self.attributes.get('shardId')
        self.stats = self.attributes.get('stats')
        self.tags = self.attributes.get('tags')
        self.title_id = self.attributes.get('titleId')
        self.season_state = self.attributes.get('seasonState')
        self.match_type = self.attributes.get('matchType')


class Roster(Domain):

    def from_dict(self):
        super().from_dict()
        self.shard_id = self.attributes.get('shardId')
        self.stats = self.attributes.get('stats')
        self.won = self.attributes.get('won')


class Participant(Domain):

    def from_dict(self):
        super().from_dict()
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
        self.kill_streaks = self.stats.get('killStreaks')
        self.kills = self.stats.get('kills')
        self.longest_kill = self.stats.get('longestKill')
        self.name = self.stats.get('name')
        self.player_id = self.stats.get('playerId')
        self.revives = self.stats.get('revives')
        self.ride_distance = self.stats.get('rideDistance')
        self.road_kills = self.stats.get('roadKills')
        self.swim_distance = self.stats.get('swimDistance')
        self.team_kills = self.stats.get('teamKills')
        self.time_survived = self.stats.get('timeSurvived')
        self.vehicle_destroys = self.stats.get('vehicleDestroys')
        self.walk_distance = self.stats.get('walkDistance')
        self.weapons_acquired = self.stats.get('weaponsAcquired')
        self.win_place = self.stats.get('winPlace')


class Asset(Domain):

    def from_dict(self):
        super().from_dict()
        self.created_at = self.attributes.get('createdAt')
        self.description = self.attributes.get('description')
        self.name = self.attributes.get('name')
        self.url = self.attributes.get('URL')


class Player(Domain):

    def from_dict(self):
        super().from_dict()
        self.name = self.attributes.get('name')
        self.patch_version = self.attributes.get('patchVersion')
        self.shard_id = self.attributes.get('shardId')
        self.stats = self.attributes.get('stats')
        self.title_id = self.attributes.get('titleId')
        self.rank = self.attributes.get('rank')


class Tournament(Domain):
    pass


class Season(Domain):

    def from_dict(self):
        super().from_dict()
        self.is_current_season = self.attributes.get('isCurrentSeason')
        self.is_off_season = self.attributes.get('isOffseason')


class Playerseason(Domain):

    def from_dict(self):
        super().from_dict()
        self.best_rank_point = self.attributes.get('bestRankPoint')
        game_mode_stats = self.attributes.get('gameModeStats')
        self.solo = Stats({'data': game_mode_stats.get('solo', {})})
        self.solo_fpp = Stats({'data': game_mode_stats.get('solo-fpp', {})})
        self.duo = Stats({'data': game_mode_stats.get('duo', {})})
        self.duo_fpp = Stats({'data': game_mode_stats.get('duo-fpp', {})})
        self.squad = Stats({'data': game_mode_stats.get('squad', {})})
        self.squad_fpp = Stats({'data': game_mode_stats.get('squad-fpp', {})})


class Stats(Domain):
    # TODO: i don't think stats is really a domain
    # but just a collection of statuses

    def from_dict(self):
        super().from_dict()
        self.assists = self._data.get('assists')
        self.boosts = self._data.get('boosts')
        self.dbnos = self._data.get('dBNOs')
        self.daily_kills = self._data.get('dailyKills')
        self.damage_dealt = self._data.get('damageDealt')
        self.days = self._data.get('days')
        self.daily_wins = self._data.get('dailyWins')
        self.headshot_kills = self._data.get('headshotKills')
        self.heals = self._data.get('heals')
        self.kills = self._data.get('kills')
        self.longest_kill = self._data.get('longestKill')
        self.longest_time_survived = self._data.get('longestTimeSurvived')
        self.losses = self._data.get('losses')
        self.max_kill_streaks = self._data.get('maxKillStreaks')
        self.most_survival_time = self._data.get('mostSurvivalTime')
        self.rank_points = self._data.get('rankPoints')
        self.rank_points_title = self._data.get('rankPointsTitle')
        self.revives = self._data.get('revives')
        self.ride_distance = self._data.get('rideDistance')
        self.road_kills = self._data.get('roadKills')
        self.round_most_kills = self._data.get('roundMostKills')
        self.rounds_played = self._data.get('roundsPlayed')
        self.suicides = self._data.get('suicides')
        self.swim_distance = self._data.get('swimDistance')
        self.team_kills = self._data.get('teamKills')
        self.time_survived = self._data.get('timeSurvived')
        self.top10s = self._data.get('top10s')
        self.vehicle_destroys = self._data.get('vehicleDestroys')
        self.walk_distance = self._data.get('walkDistance')
        self.weapons_acquired = self._data.get('weaponsAcquired')
        self.weekly_kills = self._data.get('weeklyKills')
        self.weekly_wins = self._data.get('weeklyWins')
        self.wins = self._data.get('wins')


class Leaderboard(Domain):

    def from_dict(self):
        super().from_dict()
        self.shard_id = self.attributes.get('shardId')
        self.game_mode = self.attributes.get('gameMode')


class Weaponmasterysummary(Domain):

    def from_dict(self):
        super().from_dict()
        self.platform = self.attributes.get('platform')
        self.weapon_summaries = self.attributes.get('weaponSummaries')
        self.latest_match_id = self.attributes.get('latestMatchId')
