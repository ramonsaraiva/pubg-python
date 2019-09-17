import json
import pytest
import requests_mock
from pubg_python.base import PUBG, Shard, APIClient, Telemetry
from pubg_python.domain.telemetry.events import LogMatchDefinition

api = PUBG('apikey', Shard.STEAM)
BASE_URL = APIClient.BASE_URL
TELEMETRY_URL = 'http://telemetry-cdn.playbattlegrounds.com/telemetry.json'
TELEMETRY_JSON = json.load(open('tests/telemetry_response.json'))


@pytest.fixture()
def mock():
    with requests_mock.Mocker() as mock:
        yield mock


def test_telemetry_instance(mock):
    mock.get(TELEMETRY_URL, json=TELEMETRY_JSON)
    telemetry = api.telemetry(TELEMETRY_URL)
    assert isinstance(telemetry, Telemetry)


def test_telemetry_from_json():
    telemetry = Telemetry.from_json('tests/telemetry_response.json')
    assert isinstance(telemetry, Telemetry)


def test_events_from_type(mock):
    mock.get(TELEMETRY_URL, json=TELEMETRY_JSON)
    telemetry = api.telemetry(TELEMETRY_URL)
    match_definition = telemetry.events_from_type('LogMatchDefinition')
    assert isinstance(match_definition[0], LogMatchDefinition)
    assert len(match_definition) == 1
