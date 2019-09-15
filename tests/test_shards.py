from pubg_python import PUBG, Shard

api = PUBG('apikey', Shard.STEAM)


def test_asia_shard():
    api.shard = Shard.PC_AS
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'pc-as'


def test_europe_shard():
    api.shard = Shard.PC_EU
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'pc-eu'


def test_pc_kakao_shard():
    api.shard = Shard.PC_KAKAO
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'pc-kakao'


def test_korea_shard():
    api.shard = Shard.PC_KRJP
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'pc-krjp'


def test_north_america_shard():
    api.shard = Shard.PC_NA
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'pc-na'


def test_oceania_shard():
    api.shard = Shard.PC_OC
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'pc-oc'


def test_south_central_america_shard():
    api.shard = Shard.PC_SA
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'pc-sa'


def test_south_east_asia_shard():
    api.shard = Shard.PC_SEA
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'pc-sea'


def test_japan_shard():
    api.shard = Shard.PC_JP
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'pc-jp'


def test_russia_shard():
    api.shard = Shard.PC_RU
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'pc-ru'


def test_pc_tournament_shard():
    api.shard = Shard.PC_TOURNAMENT
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'pc-tournament'


def test_xbox_asia_shard():
    api.shard = Shard.XBOX_AS
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'xbox-as'


def test_xbox_europe_shard():
    api.shard = Shard.XBOX_EU
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'xbox-eu'


def test_xbox_north_america_shard():
    api.shard = Shard.XBOX_NA
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'xbox-na'


def test_xbox_oceania_shard():
    api.shard = Shard.XBOX_OC
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'xbox-oc'


def test_xbox_south_america_shard():
    api.shard = Shard.XBOX_SA
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'xbox-sa'


def test_kakao_shard():
    api.shard = Shard.KAKAO
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'kakao'


def test_playstation_shard():
    api.shard = Shard.PSN
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'psn'


def test_steam_shard():
    api.shard = Shard.STEAM
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'steam'


def test_tournament_shard():
    api.shard = Shard.TOURNAMENT
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'tournament'


def test_xbox_shard():
    api.shard = Shard.XBOX
    assert isinstance(api._shard, Shard)
    assert api._shard.value == 'xbox'
