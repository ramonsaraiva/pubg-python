import json
import pytest
import requests_mock
from pubg_python.base import PUBG, Shard, APIClient
from pubg_python.domain.base import Match, Roster, Participant, Asset

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
    assert isinstance(match, Match)
    assert match.id == match_id
    assert isinstance(asset, Asset)
    assert isinstance(roster, Roster)
    assert isinstance(participant, Participant)