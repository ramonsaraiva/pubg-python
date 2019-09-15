from furl import furl
from pubg_python.base import PUBG, Shard, APIClient

api = PUBG('apikey', Shard.STEAM)
BASE_URL = APIClient.BASE_URL


def test_matches():
    url = furl(BASE_URL).join('shards/steam/matches').url
    assert api.matches().endpoint.url == url


def test_players():
    url = furl(BASE_URL).join('shards/steam/players').url
    assert api.players().endpoint.url == url


def test_samples():
    url = furl(BASE_URL).join('shards/steam/samples').url
    assert api.samples().endpoint.url == url


def test_tournaments():
    url = furl(BASE_URL).join('tournaments').url
    assert api.tournaments().endpoint.url == url


def test_leaderboards():
    url = furl(BASE_URL).join('shards/steam/leaderboards/game_mode').url
    assert api.leaderboards('game_mode').endpoint.url == url


def test_seasons():
    url = furl(BASE_URL).join('shards/steam/seasons').url
    assert api.seasons().endpoint.url == url


def test_seasons_with_game_mode():
    season = api.seasons(season_id='season_id', game_mode='game_mode')
    endpoint = season.endpoint
    url = furl(BASE_URL).join(
        'shards/steam/seasons/season_id/gameMode/game_mode/players').url
    assert endpoint.url == url


def test_seasons_with_player_id():
    season = api.seasons(season_id='season_id', player_id='player_id')
    endpoint = season.endpoint
    url = furl(BASE_URL).join(
        'shards/steam/players/player_id/seasons/season_id').url
    assert endpoint.url == url
