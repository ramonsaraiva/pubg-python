import json
import pytest
import requests_mock
from furl import furl
from pubg_python.base import PUBG, Shard, APIClient
from pubg_python.domain.base import Player, Match

api = PUBG('apikey', Shard.STEAM)
BASE_URL = APIClient.BASE_URL
ENDPOINT_PATH = 'shards/steam/players'


@pytest.fixture()
def mock():
    with requests_mock.Mocker() as mock:
        yield mock


@pytest.fixture()
def players_response():
    with open('tests/players_response.json') as json_file:
        yield json.load(json_file)


@pytest.fixture()
def player_response():
    with open('tests/player_response.json') as json_file:
        yield json.load(json_file)


def test_player_get(mock, player_response):
    player_id = 'account.d1c920088e124f2393455e05c11a8775'
    url = furl(BASE_URL).join(ENDPOINT_PATH + '/' + player_id).url
    mock.get(url, json=player_response)
    player = api.players().get(player_id)
    assert isinstance(player, Player)
    assert player.id == player_id


def test_player_filter_names(mock, players_response):
    player_names = ['chocoTaco', 'glmn']
    url = furl(BASE_URL).join(ENDPOINT_PATH).add(
        {'filter[playerNames]': ','.join(player_names)}).url
    mock.get(url, json=players_response)
    players = api.players().filter(player_names=player_names)
    for player in players:
        match = player.matches[0]
        assert isinstance(player, Player)
        assert player.name in player_names
        assert str(player) == player.id
        assert type(player.name) == str
        assert isinstance(match, Match)


def test_player_filter_ids(mock, players_response):
    player_ids = ['account.15cbf322a9bc45e88b0cd9f12ef4188e',
                  'account.d1c920088e124f2393455e05c11a8775']
    url = furl(BASE_URL).join(ENDPOINT_PATH).add(
        {'filter[playerIds]': ','.join(player_ids)}).url
    mock.get(url, json=players_response)
    players = api.players().filter(player_ids=player_ids)
    for player in players:
        match = player.matches[0]
        assert isinstance(player, Player)
        assert isinstance(player, Player)
        assert player.id in player_ids
        assert str(player) == player.id
        assert type(player.id) == str
        assert isinstance(match, Match)
