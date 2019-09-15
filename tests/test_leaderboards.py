import json
import pytest
import requests_mock
from furl import furl
from pubg_python.base import PUBG, Shard, APIClient
from pubg_python.domain.base import Leaderboard
from pubg_python.domain.telemetry.resources import GAME_MODE

api = PUBG('apikey', Shard.STEAM)
BASE_URL = APIClient.BASE_URL
ENDPOINT_PATH = 'shards/steam/leaderboards'


@pytest.fixture()
def mock():
    with requests_mock.Mocker() as mock:
        yield mock


@pytest.fixture()
def leaderboard_response():
    with open('tests/leaderboard_response.json') as json_file:
        yield json.load(json_file)


def test_leaderboard(mock, leaderboard_response):
    game_mode = 'squad-fpp'
    page_number = 0

    url = furl(BASE_URL).join(ENDPOINT_PATH + '/' + game_mode).add(
        {'page[number]': page_number}).url
    mock.get(url, json=leaderboard_response)
    data = api.leaderboards(game_mode=game_mode).page(page_number).get()
    assert isinstance(data, Leaderboard)
    assert data.shard_id in Shard._value2member_map_
    assert data.game_mode in GAME_MODE
