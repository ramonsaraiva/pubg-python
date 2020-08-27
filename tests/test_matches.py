import json
import pytest
import requests_mock
from pubg_python.base import PUBG, Shard, APIClient
from pubg_python.domain.base import Match, Roster, Participant, Asset
from pubg_python.domain.telemetry.resources import GAME_MODE, SEASON_STATE

api = PUBG('apikey', Shard.STEAM)
BASE_URL = APIClient.BASE_URL


@pytest.fixture()
def mock():
    with requests_mock.Mocker() as mock:
        yield mock


@pytest.fixture()
def match_response():
    with open('tests/match_response.json') as json_file:
        yield json.load(json_file)


def test_match_get(mock, match_response):
    match_id = 'f80126f4-9520-4c66-9198-57820d04bf00'
    url = '{}shards/steam/matches/{}'.format(BASE_URL, match_id)
    mock.get(url, json=match_response)
    match = api.matches().get(match_id)
    asset = match.assets[0]
    roster = match.rosters[0]
    participant = roster.participants[0]
    print(match.title_id)
    assert isinstance(match, Match)
    assert isinstance(asset, Asset)
    assert isinstance(roster, Roster)
    assert isinstance(participant, Participant)
    assert isinstance(match.created_at, str)
    assert isinstance(match.duration, int)
    assert isinstance(match.match_type, str)
    assert match.game_mode in GAME_MODE
    assert match.shard_id in Shard._value2member_map_
    assert match.season_state in SEASON_STATE
    assert match.id == match_id
