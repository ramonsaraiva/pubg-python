import json
import pytest
import requests_mock
from furl import furl
from pubg_python.base import PUBG, Shard, APIClient
from pubg_python.domain.base import Weaponmasterysummary

api = PUBG('apikey', Shard.STEAM)
BASE_URL = APIClient.BASE_URL
ENDPOINT_PATH = 'shards/steam/players/{}/weapon_mastery'


@pytest.fixture()
def mock():
    with requests_mock.Mocker() as mock:
        yield mock


@pytest.fixture()
def weapon_mastery_response():
    with open('tests/weapon_mastery_response.json') as json_file:
        yield json.load(json_file)


def test_match_get(mock, weapon_mastery_response):
    player_id = 'account.d1c920088e124f2393455e05c11a8775'
    url = furl(BASE_URL).join(ENDPOINT_PATH.format(player_id)).url
    mock.get(url, json=weapon_mastery_response)
    wm = api.weapon_mastery(player_id=player_id).get()
    assert isinstance(wm, Weaponmasterysummary)
    assert isinstance(wm.platform, str)
    assert isinstance(wm.weapon_summaries, dict)
    assert isinstance(wm.latest_match_id, str)
