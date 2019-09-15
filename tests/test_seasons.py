import json
import pytest
import requests_mock
from furl import furl
from pubg_python.base import PUBG, Shard, APIClient, QuerySet
from pubg_python.domain.base import Season, Meta, Playerseason, Stats

api = PUBG('apikey', Shard.STEAM)
BASE_URL = APIClient.BASE_URL
SEASON_PATH = 'shards/steam/seasons'
SEASON_BY_PLAYER_PATH = 'shards/steam/players/{}/seasons/{}'
SEASON_BY_PLAYERS_PATH = 'shards/steam/seasons/{}/gameMode/{}/players'


@pytest.fixture()
def mock():
    with requests_mock.Mocker() as mock:
        yield mock


@pytest.fixture()
def season_response():
    with open('tests/season_response.json') as json_file:
        yield json.load(json_file)


@pytest.fixture()
def season_playerid_response():
    with open('tests/season_playerid_response.json') as json_file:
        yield json.load(json_file)


@pytest.fixture()
def season_playerids_response():
    with open('tests/season_playerids_response.json') as json_file:
        yield json.load(json_file)


def test_season(mock, season_response):
    url = furl(BASE_URL).join(SEASON_PATH).url
    mock.get(url, json=season_response)
    seasons = api.seasons()
    seasons = [x for x in seasons]
    data = seasons[len(seasons) - 1]
    assert isinstance(data, Season)
    assert isinstance(data.is_current_season, bool)
    assert isinstance(data.is_off_season, bool)


def test_season_by_player_id(mock, season_playerid_response):
    player_id = 'account.d1c920088e124f2393455e05c11a8775'
    season_id = 'division.bro.official.pc-2018-04'
    url = furl(BASE_URL).join(SEASON_BY_PLAYER_PATH.format(
        player_id, season_id
    )).url
    mock.get(url, json=season_playerid_response)
    data = api.seasons(season_id, player_id=player_id).get()
    squad_fpp = data.squad_fpp
    assert isinstance(data, Playerseason)
    assert isinstance(data._meta, Meta)
    assert isinstance(data.solo, Stats)
    assert isinstance(data.solo_fpp, Stats)
    assert isinstance(data.duo, Stats)
    assert isinstance(data.duo_fpp, Stats)
    assert isinstance(data.squad, Stats)
    assert isinstance(data.squad_fpp, Stats)
    assert isinstance(squad_fpp.assists, int)
    assert isinstance(squad_fpp.boosts, int)
    assert isinstance(squad_fpp.dbnos, int)
    assert isinstance(squad_fpp.daily_kills, int)
    assert isinstance(squad_fpp.damage_dealt, float)
    assert isinstance(squad_fpp.days, int)
    assert isinstance(squad_fpp.daily_wins, int)
    assert isinstance(squad_fpp.headshot_kills, int)
    assert isinstance(squad_fpp.heals, int)
    assert isinstance(squad_fpp.kills, int)
    assert isinstance(squad_fpp.longest_kill, float)
    assert isinstance(squad_fpp.longest_time_survived, float)
    assert isinstance(squad_fpp.losses, int)
    assert isinstance(squad_fpp.max_kill_streaks, int)
    assert isinstance(squad_fpp.most_survival_time, float)
    assert isinstance(squad_fpp.rank_points, float)
    assert isinstance(squad_fpp.rank_points_title, str)
    assert isinstance(squad_fpp.revives, int)
    assert isinstance(squad_fpp.ride_distance, float)
    assert isinstance(squad_fpp.road_kills, int)
    assert isinstance(squad_fpp.round_most_kills, int)
    assert isinstance(squad_fpp.rounds_played, int)
    assert isinstance(squad_fpp.suicides, int)
    assert isinstance(squad_fpp.swim_distance, float)
    assert isinstance(squad_fpp.team_kills, int)
    assert isinstance(squad_fpp.time_survived, float)
    assert isinstance(squad_fpp.top10s, int)
    assert isinstance(squad_fpp.vehicle_destroys, int)
    assert isinstance(squad_fpp.walk_distance, float)
    assert isinstance(squad_fpp.weapons_acquired, int)
    assert isinstance(squad_fpp.weekly_kills, int)
    assert isinstance(squad_fpp.weekly_wins, int)
    assert isinstance(squad_fpp.wins, int)


def test_season_by_player_ids(mock, season_playerids_response):
    player_ids = ['account.d1c920088e124f2393455e05c11a8775']
    season_id = 'division.bro.official.pc-2018-04'
    game_mode = 'squad-fpp'
    url = furl(BASE_URL).join(
        SEASON_BY_PLAYERS_PATH.format(season_id, game_mode)
    ).add({'filter[playerIds]': ','.join(player_ids)}).url
    mock.get(url, json=season_playerids_response)
    players = api.seasons(
        season_id=season_id,
        game_mode=game_mode
    ).filter(player_ids=player_ids)
    data = players[0]
    squad_fpp = data.squad_fpp
    assert isinstance(players, QuerySet)
    assert isinstance(data, Playerseason)
    assert isinstance(data._meta, Meta)
    assert isinstance(data.solo, Stats)
    assert isinstance(data.solo_fpp, Stats)
    assert isinstance(data.duo, Stats)
    assert isinstance(data.duo_fpp, Stats)
    assert isinstance(data.squad, Stats)
    assert isinstance(data.squad_fpp, Stats)
    assert isinstance(squad_fpp.assists, int)
    assert isinstance(squad_fpp.boosts, int)
    assert isinstance(squad_fpp.dbnos, int)
    assert isinstance(squad_fpp.daily_kills, int)
    assert isinstance(squad_fpp.damage_dealt, float)
    assert isinstance(squad_fpp.days, int)
    assert isinstance(squad_fpp.daily_wins, int)
    assert isinstance(squad_fpp.headshot_kills, int)
    assert isinstance(squad_fpp.heals, int)
    assert isinstance(squad_fpp.kills, int)
    assert isinstance(squad_fpp.longest_kill, float)
    assert isinstance(squad_fpp.longest_time_survived, float)
    assert isinstance(squad_fpp.losses, int)
    assert isinstance(squad_fpp.max_kill_streaks, int)
    assert isinstance(squad_fpp.most_survival_time, float)
    assert isinstance(squad_fpp.rank_points, float)
    assert isinstance(squad_fpp.rank_points_title, str)
    assert isinstance(squad_fpp.revives, int)
    assert isinstance(squad_fpp.ride_distance, float)
    assert isinstance(squad_fpp.road_kills, int)
    assert isinstance(squad_fpp.round_most_kills, int)
    assert isinstance(squad_fpp.rounds_played, int)
    assert isinstance(squad_fpp.suicides, int)
    assert isinstance(squad_fpp.swim_distance, float)
    assert isinstance(squad_fpp.team_kills, int)
    assert isinstance(squad_fpp.time_survived, float)
    assert isinstance(squad_fpp.top10s, int)
    assert isinstance(squad_fpp.vehicle_destroys, int)
    assert isinstance(squad_fpp.walk_distance, float)
    assert isinstance(squad_fpp.weapons_acquired, int)
    assert isinstance(squad_fpp.weekly_kills, int)
    assert isinstance(squad_fpp.weekly_wins, int)
    assert isinstance(squad_fpp.wins, int)
