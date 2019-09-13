import pytest
import requests_mock
from pubg_python.base import *

api = PUBG('apikey', Shard.STEAM)
BASE_URL = APIClient.BASE_URL

def test_matches():
    url = BASE_URL + 'shards/steam/matches'
    assert api.matches().endpoint.url == url

def test_players():
    url = BASE_URL + 'shards/steam/players'
    assert api.players().endpoint.url == url

def test_samples():
    url = BASE_URL + 'shards/steam/samples'
    assert api.samples().endpoint.url == url

def test_tournaments():
    url = BASE_URL + 'tournaments'
    assert api.tournaments().endpoint.url == url

def test_leaderboards():
    url = BASE_URL + 'shards/steam/leaderboards/game_mode'
    assert api.leaderboards('game_mode').endpoint.url == url

def test_seasons():
    url = BASE_URL + 'shards/steam/seasons'
    assert api.seasons().endpoint.url == url

def test_seasons_with_game_mode():
    season = api.seasons(season_id='season_id', game_mode='game_mode')
    endpoint = season.endpoint
    url = BASE_URL + 'shards/steam/seasons/season_id/gameMode/game_mode/players'
    assert endpoint.url == url

def test_seasons_with_player_id():
    season = api.seasons(season_id='season_id', player_id='player_id')
    endpoint = season.endpoint
    url = BASE_URL + 'shards/steam/players/player_id/seasons/season_id'
    assert endpoint.url == url