import pytest
import requests_mock
from pubg_python.base import *
from pubg_python.domain.base import *

api = PUBG('apikey', Shard.STEAM)
BASE_URL = APIClient.BASE_URL

@pytest.fixture()
def mock():
    with requests_mock.Mocker() as mock:
        yield mock

def test_player_get(mock):
    player_id = 'player_id'
    url = '{}shards/steam/players/{}'.format(BASE_URL, player_id)
    mock.get(url, json={"data": {"type": "player", "id": player_id}})
    player = api.players().get(player_id)
    assert isinstance(player, Player)
    assert player.id == player_id

def test_player_filter_names(mock):
    player_names = ['chocoTaco', 'glmn']
    url = '{}shards/steam/players?filter%5BplayerNames%5D={}'.format(
        BASE_URL, '%2C'.join(player_names))
    json_data = [
        {
            "type": "player",
            "id": "account.15cbf322a9bc45e88b0cd9f12ef4188e",
            "attributes": {
                "name": "chocoTaco",
            },
            "relationships": {
                "assets": {"data": []},
                "matches": {"data": []}
            }
        },
        {
            "type": "player",
            "id": "account.d1c920088e124f2393455e05c11a8775",
            "attributes": {
                "name": "glmn"
            },
            "relationships": {
                "assets": {"data": []},
                "matches": {"data": []}
            }
        }]
    mock.get(url, json={'data': json_data})
    players = api.players().filter(player_names=player_names)
    for player in players:
        assert isinstance(player, Player)
        assert player.name in player_names
        assert str(player) == player.id
        assert type(player.name) == str

def test_player_filter_ids(mock):
    player_ids = ['account.15cbf322a9bc45e88b0cd9f12ef4188e',
        'account.d1c920088e124f2393455e05c11a8775']
    url = '{}shards/steam/players?filter%5BplayerIds%5D={}'.format(
        BASE_URL, '%2C'.join(player_ids))
    json_data = [
        {
            "type": "player",
            "id": "account.15cbf322a9bc45e88b0cd9f12ef4188e",
            "attributes": {
                "name": "chocoTaco",
            },
            "relationships": {
                "assets": {"data": []},
                "matches": {"data": []}
            }
        },
        {
            "type": "player",
            "id": "account.d1c920088e124f2393455e05c11a8775",
            "attributes": {
                "name": "glmn"
            },
            "relationships": {
                "assets": {"data": []},
                "matches": {"data": []}
            }
        }]
    mock.get(url, json={'data': json_data})
    players = api.players().filter(player_ids=player_ids)
    for player in players:
        assert isinstance(player, Player)
        assert player.id in player_ids
        assert str(player) == player.id
        assert type(player.id) == str