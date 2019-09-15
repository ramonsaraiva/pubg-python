import json
import pytest
import requests_mock
from furl import furl
from pubg_python.base import PUBG, Shard, APIClient
from pubg_python.domain.base import Sample, Match

api = PUBG('apikey', Shard.STEAM)
BASE_URL = APIClient.BASE_URL
ENDPOINT_PATH = 'shards/steam/samples'


@pytest.fixture()
def mock():
    with requests_mock.Mocker() as mock:
        yield mock


@pytest.fixture()
def samples_response():
    with open('tests/samples_response.json') as json_file:
        yield json.load(json_file)


def test_match_get(mock, samples_response):
    match_id = '3095f3be-a327-491c-be17-6e4823821b2e'
    url = furl(BASE_URL).join(ENDPOINT_PATH).url
    mock.get(url, json=samples_response)
    sample = api.samples().get()
    match = sample.matches[0]
    assert isinstance(sample, Sample)
    assert isinstance(match, Match)
    assert match.id == match_id


def test_match_filter_created_at_start(mock, samples_response):
    created_at = '2019-09-14T00:00:00Z'
    match_id = '3095f3be-a327-491c-be17-6e4823821b2e'
    url = furl(BASE_URL).join(ENDPOINT_PATH).add(
        {'filter[createdAt-start]': created_at}).url
    mock.get(url, json=samples_response)
    sample = api.samples().filter(created_at_start=created_at).get()
    match = sample.matches[0]
    assert isinstance(sample, Sample)
    assert isinstance(match, Match)
    assert match.id == match_id
