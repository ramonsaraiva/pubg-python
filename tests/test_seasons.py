import json
import pytest
import requests_mock
from furl import furl
from pubg_python.base import PUBG, Shard, APIClient
from pubg_python.domain.base import Season

api = PUBG('apikey', Shard.STEAM)
BASE_URL = APIClient.BASE_URL
ENDPOINT_PATH = 'shards/steam/seasons'


@pytest.fixture()
def mock():
    with requests_mock.Mocker() as mock:
        yield mock


@pytest.fixture()
def season_response():
    with open('tests/season_response.json') as json_file:
        yield json.load(json_file)


def test_season(mock, season_response):
    url = furl(BASE_URL).join(ENDPOINT_PATH).url
    mock.get(url, json=season_response)
    seasons = api.seasons()
    seasons = [x for x in seasons]
    print(seasons[0].is_current_season)
    data = seasons[len(seasons) - 1]
    print(vars(data))
    assert isinstance(data, Season)
    assert isinstance(data.is_current_season, bool)
    assert isinstance(data.is_off_season, bool)
