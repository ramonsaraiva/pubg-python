import pytest
import requests_mock
from pubg_python.base import PUBG, Shard, APIClient
from pubg_python.exceptions import (
    APIError,
    InvalidShardError,
    InvalidFilterError,
    RequiredFilterError,
    UnauthorizedError,
    NotFoundError,
    InvalidContentTypeError,
    RateLimitError,
    OldTelemetryError,
    TelemetryURLError
)
api = PUBG('apikey', Shard.STEAM)
BASE_URL = APIClient.BASE_URL


@pytest.fixture()
def mock():
    with requests_mock.Mocker() as mock:
        yield mock


def test_invalid_shard_error():
    try:
        api.shard = 'invalid_shard'
    except InvalidShardError:
        assert True


def test_invalid_filter_error():
    try:
        api.players().filter(player_kills=100)
        assert False
    except InvalidFilterError:
        assert True


def test_required_filter_error():
    try:
        api.seasons(season_id='season_id')
    except RequiredFilterError:
        assert True


def test_api_error():
    try:
        api.matches().get('wrong_id')
        assert False
    except APIError:
        assert True


def test_client_unauthorized_error(mock):
    url = '{}shards/steam/matches/{}'.format(BASE_URL, 'match_id')
    mock.get(url, status_code=401)
    try:
        api.matches().get('match_id')
        assert False
    except UnauthorizedError:
        assert True


def test_client_notfound_error(mock):
    url = '{}shards/steam/matches/{}'.format(BASE_URL, 'match_id')
    mock.get(url, status_code=404)
    try:
        api.matches().get('match_id')
        assert False
    except NotFoundError:
        assert True


def test_client_invalid_content_type_error(mock):
    url = '{}shards/steam/matches/{}'.format(BASE_URL, 'match_id')
    mock.get(url, status_code=415)
    try:
        api.matches().get('match_id')
        assert False
    except InvalidContentTypeError:
        assert True


def test_client_ratelimit_error(mock):
    url = '{}shards/steam/matches/{}'.format(BASE_URL, 'match_id')
    headers = {'X-Ratelimit-Limit': '9', 'X-Ratelimit-Reset': '50'}
    mock.get(url, status_code=429, headers=headers)
    try:
        api.matches().get('match_id')
        assert False
    except RateLimitError:
        assert True


def test_old_telemetry_error(mock):
    url = 'https://telemetry-cdn.playbattlegrounds.com/missed_path.json'
    mock.get(url, status_code=403)
    try:
        api.telemetry(url)
        assert False
    except OldTelemetryError:
        assert True


def test_telemetry_url_error(mock):
    url = 'https://different-host.com/telemetry.json'
    mock.get(url, status_code=200)
    try:
        api.telemetry(url)
        assert False
    except TelemetryURLError:
        assert True
